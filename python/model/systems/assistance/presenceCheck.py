import logging,inject
import datetime
from model.systems.assistance.date import Date
from model.systems.assistance.schedule import Schedule

'''
Tipo de chequeo PRESENCE
'''
class PresenceCheck:

    date = inject.attr(Date)
    schedule = inject.attr(Schedule)

    type = 'PRESENCE'
    check = None

    def __init__(self, userId, start):
        self.check = {
            'start':start,
            'end':None,
            'type':self.type
        }


    @classmethod
    def create(cls,id,userId,start,cur):
        return cls(userId,start)

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

        logging.debug('presencia {} {}'.format(userId,actualDateUtc))

        logs = self.schedule.getLogsForSchedule(con,userId,actualDateUtc)

        fails = []

        if (logs is None) or (len(logs) <= 0):

            fail = {
                    'userId':userId,
                    'date':actualDate,
                    'description':'Sin marcación',
                    'justifications':justifications
                   }
            fails.append(fail)

        return fails
