import logging,inject
import datetime
from model.systems.assistance.date import Date
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.logs import Logs
from model.systems.asssitance.check.check import Check

'''
Tipo de chequeo HOURS
'''
class HoursCheck(Check):

    date = inject.attr(Date)
    schedule = inject.attr(Schedule)
    logs = inject.attr(Logs)

    type = 'HOURS'

    def create(self,id,userId,start,cur):
        check = {
            'userId': userId,
            'start':start,
            'end':None,
            'type':self.type
        }
        check['hours'] = self.getHoursCheck(id,cur)
        return check

    def isTypeCheck(self,type):
        return self.type == type

    def isActualCheck(self,date,start,end):
        if (date >= start):
            if end is None:
                return True
            elif date < end:
                return True
        return false

    def getHoursCheck(self,id,cur):
        cur.execute('select hours from assistance.hours_check where id = %s',(c[0],))
        h = cur.fetchone()
        return h[0]

    '''
        return
        fail: {
            'userId':'',
            'date':date,
            'description':'Sin marcación',
            'justifications':[]
        }
        actualDate es aware.
    '''
    def getFails(self, utils, userId, actualDate, justifications, con):
        actualDateUtc = self.date.awareToUtc(actualDate)

        fails = []

        logging.debug('horas {} {}'.format(userId,actualDateUtc))

        logs = self.schedule.getLogsForSchedule(con,userId,actualDateUtc)
        whs,attlogs = self.logs.getWorkedHours(logs)

        count = 0
        for wh in whs:
            count = count + wh['seconds']
        if count < (self.check['hours'] * 60 * 60):

            fail = {
                    'userId':userId,
                    'date':actualDate,
                    'description':'No trabajó la cantidad mínima de minutos requeridos ({} < {})'.format(count / 60, check['hours'] * 60),
                    'justifications':justifications
                   }
            fail.append(fail)

        return fails
