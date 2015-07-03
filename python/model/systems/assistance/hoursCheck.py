import logging,inject
import datetime
from model.systems.assistance.date import Date
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.logs import Logs

'''
Tipo de chequeo HOURS
'''
class HoursCheck:

    date = inject.attr(Date)
    schedule = inject.attr(Schedule)
    logs = inject.attr(Logs)

    type = 'HOURS'
    check = None

    def __init__(self, userId, start, hours):
        self.check = {
            'start':start,
            'end':None,
            'type':self.type,
            'hours': hours
        }


    @classmethod
    def create(cls,id,userId,start,cur):
        cur.execute('select hours from assistance.hours_check where id = %s',(c[0],))
        h = cur.fetchone()
        return cls(userId,start,h[0])

    @classmethod
    def isTypeCheck(cls,type):
        return cls.type == type

    def isActualCheck(self,date):
        if (date >= self.check['start']):
            if self.check['end'] is None:
                return True
            elif date < self.check['end']:
                return True
        return False


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
