# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid

from model.systems.assistance.justifications.justification import Justification, Repetition
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.justifications.exceptions import *


"""
    Boletas de salida - restricciones en horas.
    anuales 36 horas
    mensuales 3 horas
    semanales 3 horas
    diario 3 horas
"""
class BSJustification(Justification):

    id = 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'

    def isJustification(self,id):
        return self.id == id

    """
        retorna la cantidad de justificaciones que se tienen disponibles dentro de un período de tiempo.
        si period = None entonces tiene en cuenta todos los períodos y toma el mínimo.
        period = 'MONTH|YEAR|WEEK'
    """
    def available(self,utils,con,userId,date,period=None):
      date = datetime.datetime(2015, 5, 15)
      if period == 'YEAR':
        return self._availableYear(utils,con,userId,date)
      else:
        return self._availableMonth(utils,con,userId,date)


    """
     " Calcular stock mensual
     """
    def _availableMonth(self,utils,con,userId,date):
      ##### chequeo rapido inicial: Se verifican si existen solicitudes de justificaciones pendientes o aprobadas #####
      justStatus = utils._getJustificationsInStatus(con,['PENDING','APPROVED'])
      if len(justStatus) <= 0:
        return _availableRep(self,Repetition.MONTH,userId,date);
      
      ##### consultar solicitudes de justificaciones del usuario en el mes #####
      justIds = tuple(justStatus.keys())

      cur = con.cursor()
      req = (self.id, userId, justIds, date, date)
      cur.execute("""
        SELECT jbegin,jend 
        FROM assistance.justifications_requests 
        WHERE justification_id = %s 
        AND user_id = %s 
        AND id IN %s 
        AND extract(year from jbegin) = extract(year from %s) 
        AND extract(month from jbegin) = extract(month from %s)
      """,req)
      
      if(cur.rowcount <= 0):
        return _availableRep(self,Repetition.MONTH,userId,date);

      requestJustifications = cur.fetchall();


      for rj in requestJustifications:
        sch = Schedule()
        schedule = sch.getSchedule(con, userId, rj[0])
        print(schedule)
        
      return cur.rowcount * 2000

    """
     " Calcular stock anual
     """      
    def _availableYear(self,utils,con,userId,date):
      ##### chequeo rapido inicial: Se verifican si existen solicitudes de justificaciones pendientes o aprobadas #####
      justStatus = utils._getJustificationsInStatus(con,['PENDING','APPROVED'])
      if len(justStatus) <= 0:
        _availableRep(self,Repetition.YEARLY,userId,date);
      
      return 1000
       


    """ retorna las disponibles por restricciones en la fecha date """
    def _availableRep(self,rep,userId,date):
        if rep is Repetition.YEARLY:
            return ((13 - date.month) * datetime.timedelta(hours=3)).total_seconds()

        return datetime.timedelta(hours=3).total_seconds()



    """
        inicializa un pedido en estado pendiente de una justificación en las fechas indicadas
    """
    def requestJustification(self,utils,con,userId,requestor_id,begin,end):

        available = self.available(utils,con,userId,begin)

        if available < (end-begin).total_seconds():
            raise RestrictionError('No existe stock disponible')

        jid = str(uuid.uuid4())
        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into assistance.justifications_requests (id,user_id,requestor_id,justification_id,jbegin,jend) values (%s,%s,%s,%s,%s,%s)',(jid,userId,requestor_id,self.id,begin,end))

        events = []
        e = {
            'type':'JustificationsRequestsUpdatedEvent',
            'data':{
                'justification_id':self.id,
                'user_id':userId
            }
        }
        events.append(e)


        req = {
            'id':jid,
            'user_id':userId,
            'justification_id':self.id,
            'begin':begin,
            'end':end
        }

        events.extend(self.updateJustificationRequestStatus(utils,con,userId,req,'PENDING'))
        return events



    """ actualiza el estado del pedido de la justificacion al estado status """
    def updateJustificationRequestStatus(self,utils,con,userId,req,status):

        requestId = req['id']

        cur = con.cursor()
        cur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status) values (%s,%s,%s)',(requestId,userId,status))

        events = []
        e = {
            'type':'JustificationStatusChangedEvent',
            'data':{
                'request_id':requestId,
                'status':status
            }
        }
        events.append(e)

        e = {
            'type':'JustificationStockChangedEvent',
            'data':{
                'justification_id':self.id,
                'user_id':req['user_id']
            }
        }
        events.append(e)

        return events
