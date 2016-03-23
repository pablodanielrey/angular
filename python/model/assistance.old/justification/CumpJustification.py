# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid

from model.assistance.justification.justification import Justification, Repetition
from model.assistance.justification.exceptions import *


"""
    Cumpleaños
    anuales 1
    mensuales 1
    semanales 1
"""
class CumpJustification(Justification):

    id = 'b309ea53-217d-4d63-add5-80c47eb76820'

    def isJustification(self,id):
        return self.id == id

    def _isJustifiedDay(self,date):
        return True

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
            return 1

        if rep is Repetition.WEEKLY:
            if self._weekChangesMonth(date):
                return 1
            else:
                return 1

        if rep is Repetition.MONTHLY:
            return 1

        if rep is Repetition.YEARLY:
            return 1

        return None



    """
        inicializa un pedido en estado pendiente de una justificación en las fechas indicadas
        solo se tiene en cuenta begin
    """
    def requestJustification(self,utils,con,userId,requestor_id,begin,end,status):
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

        created = datetime.datetime.now()
        aux = created - datetime.timedelta(seconds=60)
        e = self.updateJustificationRequestStatus(utils,con,userId,req,'PENDING',aux)
        if status != None and status != 'PENDING':
            e = self.updateJustificationRequestStatus(utils,con,userId,req,status)
        events.extend(e)
        return events



    """ actualiza el estado del pedido de la justificacion al estado status """
    def updateJustificationRequestStatus(self,utils,con,userId,req,status,created=None):
        if created is None:
            created = datetime.datetime.now(datetime.timezone.utc)
            created = created - datetime.timedelta(seconds=1)

        requestId = req['id']

        cur = con.cursor()
        cur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status,created) values (%s,%s,%s,%s)',(requestId,userId,status,created))

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
