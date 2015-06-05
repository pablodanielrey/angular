# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid

from model.systems.assistance.justifications.justification import Justification, Repetition
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.logs import Logs
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
    totalStock = 10800 #stock mensual en segundos

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
      ##### chequeo inicial: Se verifican si existen solicitudes de justificaciones pendientes o aprobadas #####
      justStatus = utils._getJustificationsInStatus(con,['PENDING','APPROVED'])
      if len(justStatus) <= 0:
        return self.totalStock
      
      ##### consultar solicitudes de justificaciones del usuario en el mes #####
      justIds = tuple(justStatus.keys())

      cur = self._getCursorUserRequestedJustificationMonth(con, userId, justIds, date)
      
      if(cur.rowcount <= 0):
        return self.totalStock

      requestJustifications = cur.fetchall();

      stock = self.totalStock
      for rj in requestJustifications:
        if (stock <= 0):
          break;

        schedule = Schedule()
        userSchedule = schedule.getSchedule(con, userId, rj[0])
        for schLog in userSchedule:
          if (stock <= 0):
            break;
            
          #si existe un schLog asociado al rj se deben verificar los logs realizados por el usuario para efectuar el calculo
          if schLog["start"] <= rj[0] and schLog["end"] >= rj[1]:
            stock = self._getStockFromLogs(stock, rj, schLog, userSchedule);

          #si no existe un schLog asociado al rj se resta del stock las fechas del rj
          else:
            stock = self._getStockFromDates(stock, rj[0], rj[1])
          

      return stock


    """
     "
     """
    def _getCursorUserRequestedJustificationMonth(self, con, userId, justIds, date):
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
      return cur
     
    """
     " Calcular stock a partir de un valor inicial y el chequeo del logs
    """
    def _getStockFromLogs(self, stock, rj, schLog, userSchedule):
      #obtener fechas mas inicial y fecha mas final del userSchedule
      #calcular logs totales en base a los schedules     
      #consultar logs a traves de la fecha inicial y fecha mas final
      #...
      
      
      
      logs = Logs()
    
      return 1000
      
      
    """
     " Calcular stock a partir de un valor inicial y dos dates: Se tomara la diferencia en segundos de los dates y se restara al valor inicial
     """
    def _getStockFromDates(self, stock, date1, date2):
      diffAux = (date1 - date2).total_seconds()
      diff = abs(diffAux)
      newStock = (stock-diff)
      return newStock if (newStock > 0) else 0

    
    
    """
     " Calcular stock anual
     """      
    def _availableYear(self,utils,con,userId,date):
      ##### chequeo rapido inicial: Se verifican si existen solicitudes de justificaciones pendientes o aprobadas #####
      justStatus = utils._getJustificationsInStatus(con,['PENDING','APPROVED'])
      if len(justStatus) <= 0:
        self._availableRep(Repetition.YEARLY,userId,date);
      
      return 10000
       


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
