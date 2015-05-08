# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid

from model.systems.assistance.justifications.justification import Justification, Repetition
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

        justStatus = utils._getJustificationsInStatus(con,['PENDING','APPROVED'])
        if len(justStatus) <= 0:
            """ no se tomo ninguna todavia """
            if period is None:
                return self._availableRep(Repetition.DAILY,userId,date)
            elif period == 'WEEK':
                return self._availableRep(Repetition.WEEKLY,userId,date)
            elif period == 'MONTH':
                return self._availableRep(Repetition.MONTHLY,userId,date)
            elif period == 'YEAR':
                return self._availableRep(Repetition.YEARLY,userId,date)

        justIds = tuple(justStatus.keys())

        cur = con.cursor()
        req = (self.id, userId, justIds, date, date)
        cur.execute('select jbegin,jend from assistance.justifications_requests where justification_id = %s and user_id = %s and id in %s and extract(year from jbegin) = extract(year from %s) and extract(month from jbegin) >= extract(month from %s)',req)
        takenInRestOfYear = cur.rowcount

        if takenInRestOfYear <= 0:
            """ no se tomo ninguna todavia """
            if period is None:
                return self._availableRep(Repetition.DAILY,userId,date)
            elif period == 'WEEK':
                return self._availableRep(Repetition.WEEKLY,userId,date)
            elif period == 'MONTH':
                return self._availableRep(Repetition.MONTHLY,userId,date)
            elif period == 'YEAR':
                return self._availableRep(Repetition.YEARLY,userId,date)


        datesC = cur.fetchall()
        dates = map(lambda x: x[0],datesC)
        sameMonthDates = self._filterInSameMonth(date,dates)

        secondsInYear = 0
        secondsInMonth = 0
        for bs in datesC:
            secondsInYear = secondsInYear + (bs[1]-bs[0]).total_seconds()
            if bs[0] in sameMonthDates:
                secondsInMonth = secondsInMonth + (bs[1]-bs[0]).total_seconds()


        if period == 'YEAR':
            return self._availableRep(Repetition.YEARLY,userId,date) - secondsInYear

        available = self._availableRep(Repetition.MONTHLY,userId,date) - secondsInMonth
        return available



    """ retorna las disponibles por restricciones en la fecha date """
    def _availableRep(self,rep,userId,date):
        if rep is Repetition.YEARLY:
            return ((13 - date.month) * datetime.timedelta(hours=3)).total_seconds()

        return datetime.timedelta(hours=3).total_seconds()



    """
        inicializa un pedido en estado pendiente de una justificación en las fechas indicadas
    """
    def requestJustification(self,utils,con,userId,begin,end):

        available = self.available(utils,con,userId,begin)

        if available < (end-begin).total_seconds():
            raise RestrictionError('No existe stock disponible')

        jid = str(uuid.uuid4())
        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into assistance.justifications_requests (id,user_id,justification_id,jbegin,jend) values (%s,%s,%s,%s,%s)',(jid,userId,self.id,begin,end))

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
