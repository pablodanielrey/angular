import logging,inject
import datetime
from model.systems.assistance.date import Date
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.logs import Logs

'''
Tipo de chequeo SCHEDULE
'''
class ScheduleCheck:

    date = inject.attr(Date)
    schedule = inject.attr(Schedule)
    logs = inject.attr(Logs)

    type = 'SCHEDULE'
    check = None
    tolerancia = datetime.timedelta(minutes=16)

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

        logging.debug('schedule {} {}'.format(userId,actualDateUtc))

        fails = utils.checkSchedule(con,userId,actualDateUtc)
        for f in fails:
            f['justifications'] = justifications
        return fails


    '''
        chequea los schedules contra las workedhours calculadas
    '''
    @classmethod
    def checkWorkedHours(cls,userId,controls):
        fails = []

        for sched,wh in controls:

            if sched is None:
                ''' no tiene schedule a controlar '''
                continue

            date = sched['start']

            if (wh is None) or ('start' not in wh and 'end' not in wh):
                ''' no tiene nada trabajado!!! '''
                fails.append(
                    {
                        'userId':userId,
                        'date':date,
                        'description':'Sin marcación'
                    }
                )
                continue



            ''' controlo la llegada '''
            if wh['start'] is None:
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Sin entrada'
                    }
                )

            elif wh['start'] > sched['start'] + cls.tolerancia:
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Llegada tardía',
                        'startSchedule':sched['start'],
                        'start':wh['start'],
                        'seconds':(wh['start'] - sched['start']).total_seconds(),
                        'whSeconds':wh['seconds']
                    }
                )


            ''' controlo la salida '''
            if wh['end'] is None:
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Sin salida'
                    }
                )

            elif wh['end'] < sched['end'] - cls.tolerancia:
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Salida temprana',
                        'endSchedule':sched['end'],
                        'end':wh['end'],
                        'seconds':(sched['end']-wh['end']).total_seconds(),
                        'whSeconds':wh['seconds']
                    }
                )

        return fails
