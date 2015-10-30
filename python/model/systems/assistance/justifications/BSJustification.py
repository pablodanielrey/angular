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
        
        @param date Fecha de chequeo
    """
    def _isJustifiedTimeStart(self,sched,whs,justification,tolerancia, date = None):
        start = whs[0]['start']
        if sched.getStart(date) >= justification['begin'] and start <= justification['end']:
            return True
        return False

    """
        
        @param date Fecha de chequeo
    """
    def _isJustifiedTimeEnd(self,sched,whs, justification, tolerancia, date = None):
        whEnd = whs[-1]['end']
        if whEnd >= justification['begin'] and sched.getEnd(date) <= justification['end']:
            return True
        return False


    def _isJustifiedTime(self,justification,start,end):
        if 'begin' not in justification or 'end' not in justification or start is None or end is None:
            return False
        if start >= justification['begin'] and end <= justification['end']:
            return True
            
        return False

    """
        retorna la cantidad de justificaciones que se tienen disponibles dentro de un período de tiempo.
        si period = None entonces tiene en cuenta todos los períodos y toma el mínimo.
        period = 'MONTH|YEAR|WEEK'
    """
    def available(self,utils,con,userId,date,period=None):

      #date = datetime.datetime(2015, 5, 1) #dato de prueba para el mes anterior que tiene mas logs
      if period == 'YEAR':
        return self._availableYear(utils,con,userId,date)
      else:
        return self._availableMonth(utils,con,userId,date)


    """
     " Calcular stock anual
     " @param utils Herramientas
     " @param con Conexion con la base de datos
     " @param userId Identificacion de usuario
     " @param date Fecha de consulta
     """
    def _availableYear(self,utils,con,userId,date):
      ##### definir stock inicial con el total restante #####
      stock =  (13 - date.month) * self.totalStock

      ##### chequeo rapido inicial: Se verifican si existen solicitudes de justificaciones pendientes o aprobadas #####
      justStatus = utils._getJustificationsInStatus(con,['PENDING','APPROVED'])

      if len(justStatus) <= 0:
        return stock


      ##### consultar solicitudes de justificaciones del usuario en restantes #####
      justIds = tuple(justStatus.keys())
      cur = self._getCursorUserRequestedJustificationYear(con, userId, justIds, date)

      ##### chequeo de solicitudes de justificaciones del usuario en el mes #####
      if(cur.rowcount <= 0):
        return stock

      ##### procesar las solicitudes de justificaciones del usuario #####
      requestJustifications = cur.fetchall();


      return self._availableRequestedJustifications(requestJustifications, stock, userId, con)



    """
     " Calcular stock mensual
     " @param utils Herramientas
     " @param con Conexion con la base de datos
     " @param userId Identificacion de usuario
     " @param date Fecha de consulta
     """
    def _availableMonth(self,utils,con,userId,date):
      ##### definir stock inicial con el total #####
      stock = self.totalStock

      ##### chequeo inicial: Se verifican si existen solicitudes de justificaciones pendientes o aprobadas #####
      justStatus = utils._getJustificationsInStatus(con,['PENDING','APPROVED'])
      if len(justStatus) <= 0:
        return stock


      ##### consultar solicitudes de justificaciones del usuario en el mes #####
      justIds = tuple(justStatus.keys())
      cur = self._getCursorUserRequestedJustificationMonth(con, userId, justIds, date)


      ##### chequeo de solicitudes de justificaciones del usuario en el mes #####
      if(cur.rowcount <= 0):
        return stock


      ##### procesar las solicitudes de justificaciones del usuario #####
      requestJustifications = cur.fetchall();
      return self._availableRequestedJustifications(requestJustifications, stock, userId, con)


    """
     " Procesar las solicitudes de justificaciones del usuario
     " @param requestedJustifications Solicitudes de justificaciones del usuario
     " @param stock Stock inicial
     " @param userId Identificacion de usuario
     " @param con Conexion con la base de datos
     """
    def _availableRequestedJustifications(self, requestJustifications, stock, userId, con):
      for rj in requestJustifications:
        if (stock <= 0):
          break;


        ##### comparar las solicitud de boleta con los elementos del schedule para determinar el schedule asociado a la solicitud #####
        schedule = Schedule()
        userSchedule = schedule.getSchedule(con, userId, rj[0])


        for index, usrSch in enumerate(userSchedule):
          if (stock <= 0):
            break;

          #si existe un elemento del schedule asociado a la solicitud de boleta se deben verificar los logs realizados por el usuario para efectuar el calculo
          if usrSch["start"] <= rj[0] and usrSch["end"] >= rj[1]:
            stock = self._getStockFromLogs(con, userId, stock, rj, index, userSchedule);

          #si no existe un schLog asociado a la solicitud de boleta se resta del stock las fechas de la solicitud
          else:
            stock = self._getStockFromDates(stock, rj[0], rj[1])

      return stock


    """
    " Consultar solicitudes del usuario en el mes de la fecha pasada como parametro
    """
    def _getCursorUserRequestedJustificationMonth(self, con, userId, justIds, date):
      cur = con.cursor()
      req = (self.id, userId, justIds, date, date)
      cur.execute("SELECT jbegin,jend FROM assistance.justifications_requests WHERE justification_id = %s AND user_id = %s AND id IN %s AND extract(year from jbegin) = extract(year from %s) AND extract(month from jbegin) = extract(month from %s)",req)
      return cur

    """
    " Consultar solicitudes del usuario a partir del mes de la fecha pasada como parametro y los meses restantes
    """
    def _getCursorUserRequestedJustificationYear(self, con, userId, justIds, date):
      cur = con.cursor()
      req = (self.id, userId, justIds, date, date)
      cur.execute("SELECT jbegin,jend FROM assistance.justifications_requests WHERE justification_id = %s AND user_id = %s AND id IN %s AND extract(year from jbegin) = extract(year from %s) AND extract(month from jbegin) >= extract(month from %s)",req)
      return cur



    """
     " Calcular stock a partir de un valor inicial y el chequeo del logs
     " @param con Conexion
     " @param userId Id de usuario
     " @param stock Stock inicial
     " @param requestedJustification Solicitud de justificacion
     " @param schLogIndex indice del schedule asociado a la requestedJustification
     " @param userSchedule schedule del usuario
    """
    def _getStockFromLogs(self, con, userId, stock, rj, schIndex, userSchedule):

      #definir cantidad de "user worked hours" que deberia tener el usuario
      uwhLen = len(userSchedule)
      if rj[0] != userSchedule[schIndex]["start"] and rj[1] != userSchedule[schIndex]["end"]:
        uwhLen += 1


      #obtener fecha mas inicial del userSchedule (se supone que el userSchedule esta ordenado!)
      start = userSchedule[0]["start"]

      schedule = Schedule()
      userLogs = schedule.getLogsForSchedule(con, userId, start)

      logs = Logs()
      uwhInfo = logs.getWorkedHours(userLogs)
      uwh = uwhInfo[0]

      if uwhLen != len(uwh):
        return  self._getStockFromDates(stock, rj[0], rj[1])

      #definir fechas para calculo del tiempo trabajado en la worked hour correspondiente
      if rj[0] != userSchedule[schIndex]["start"] and rj[1] != userSchedule[schIndex]["end"]:
        calcStart = uwh[schIndex]["end"]
        calcEnd =  uwh[schIndex+1]["start"]

      else:
        if(rj[0] == userSchedule[schIndex]["start"]):
          calcStart = userSchedule[schIndex]["start"]
          calcEnd = uwh[schIndex]["start"]
        else:
          calcStart = uwh[schIndex]["end"]
          calcEnd =  userSchedule[schIndex]["end"]

      #chequear si calcStart y calcEnd son distintos de None
      if calcStart is None or calcEnd is None:
          return  self._getStockFromDates(stock, rj[0], rj[1])

      #comparar diferencias de log y diferencia de boleta de salida, se restara la menor al stock
      differenceLog = (calcEnd - calcStart).total_seconds()
      differenceRj = (rj[1] - rj[0]).total_seconds()
      difference = differenceLog if (differenceLog <= differenceRj) else differenceRj

      return stock - difference





    """
     " Calcular stock a partir de un valor inicial y dos dates: Se tomara la diferencia en segundos de los dates y se restara al valor inicial
     """
    def _getStockFromDates(self, stock, date1, date2):
      diffAux = (date1 - date2).total_seconds()
      diff = abs(diffAux)
      newStock = (stock-diff)
      return newStock if (newStock > 0) else 0





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
