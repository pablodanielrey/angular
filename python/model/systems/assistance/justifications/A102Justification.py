# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid
import inject
from model.systems.assistance.justifications.justification import Justification, Repetition
from model.systems.assistance.justifications.exceptions import *
from model.systems.assistance.logs import Logs


"""
    Articulo 102
    anuales 5
    mensuales 5
    semanales 5
"""
class A102Justification(Justification):
    logs = inject.attr(Logs)

    id = '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'

    def isJustification(self,id):
        return self.id == id

    def _isJustifiedTimeEnd(self,sched,whs,justification,tolerancia):
        (sdate,edate,totalSeconds) = self.logs.explainWorkedHours(whs)
        if (totalSeconds/60) >= 120:
            return True
        return False

    def _isJustifiedTime(self,justification,start,end):
        return False

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
                return self._availableRep(Repetition.WEEKLY,userId,date)
            elif period == 'MONTH':
                return self._availableRep(Repetition.MONTHLY,userId,date)
            elif period == 'YEAR':
                return self._availableRep(Repetition.YEARLY,userId,date)


        justIds = tuple(justStatus.keys())

        cur = con.cursor()
        req = (self.id, userId, justIds, date)
        cur.execute('select jbegin from assistance.justifications_requests where justification_id = %s and user_id = %s and id in %s and extract(year from jbegin) = extract(year from %s)',req)
        taken = cur.rowcount

        if taken <= 0:

            """ no se tomo ninguna todavia """
            if period is None:
                return self._availableRep(Repetition.DAILY,userId,date)
            elif period == 'WEEK':
                return self._availableRep(Repetition.WEEKLY,userId,date)
            elif period == 'MONTH':
                return self._availableRep(Repetition.MONTHLY,userId,date)
            elif period == 'YEAR':
                return self._availableRep(Repetition.YEARLY,userId,date)


        else:
            availableInYear = self._availableRep(Repetition.YEARLY,userId,date)
            if availableInYear <= taken:
                return 0
            elif period == 'YEAR':
                return availableInYear - taken


            datesC = cur.fetchall()
            dates = map(lambda x: x[0],datesC)

            sameMonth = self._filterInSameMonth(date,dates)
            takenInMonth = len(sameMonth)
            availableInMonth = self._availableRep(Repetition.MONTHLY,userId,date)
            if availableInMonth <= takenInMonth:
                return 0
            elif period == 'MONTH':
                return availableInMonth - takenInMonth

            sameWeek = self._filterInSameWeek(date,dates)
            takenInWeek = len(sameWeek)
            availableInWeek = self._availableRep(Repetition.WEEKLY,userId,date)
            if availableInWeek <= takenInWeek:
                return 0
            elif period == 'WEEK':
                return availableInWeek - takenInWeek

            available = min(min((availableInYear - taken), availableInMonth - takenInMonth), availableInWeek - takenInWeek)
            return available



    """ retorna las disponibles por restricciones en la fecha date """
    def _availableRep(self,rep,userId,date):
        if rep is Repetition.DAILY:
            return 5

        if rep is Repetition.WEEKLY:
            if self._weekChangesMonth(date):
                return 5
            else:
                return 5

        if rep is Repetition.MONTHLY:
            return 5

        if rep is Repetition.YEARLY:
            return 5

        return None



    """
        inicializa un pedido en estado pendiente de una justificación en las fechas indicadas
        solo se tiene en cuenta begin
    """
    def requestJustification(self,utils,con,userId,requestor_id,begin,end):
        if self.available(utils,con,userId,begin) <= 0:
            raise RestrictionError('No existe stock disponible')

        jid = str(uuid.uuid4())
        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into assistance.justifications_requests (id,user_id,requestor_id,justification_id,jbegin) values (%s,%s,%s,%s,%s)',(jid,userId,requestor_id,self.id,begin))

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
