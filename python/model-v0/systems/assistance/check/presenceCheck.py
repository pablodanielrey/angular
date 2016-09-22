import logging,inject
import datetime
from model.systems.assistance.date import Date
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.check.check import Check

'''
Tipo de chequeo PRESENCE
'''
class PresenceCheck(Check):

    date = inject.attr(Date)
    schedule = inject.attr(Schedule)

    type = 'PRESENCE'

    def create(self,id,userId,start,cur):
        check = {
            'userId': userId,
            'start':start,
            'end':None,
            'type':self.type
        }
        return check

    def isTypeCheck(self,type):
        return self.type == type


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
