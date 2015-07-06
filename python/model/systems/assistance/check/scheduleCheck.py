import logging,inject
import datetime
from model.systems.assistance.date import Date
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.logs import Logs
from model.systems.asssitance.check.check import Check

'''
Tipo de chequeo SCHEDULE
'''
class ScheduleCheck(Check):

    date = inject.attr(Date)
    schedule = inject.attr(Schedule)
    logs = inject.attr(Logs)

    type = 'SCHEDULE'
    tolerancia = datetime.timedelta(minutes=16)


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

    def isActualCheck(self,date,start,end):
        if (date >= start):
            if end is None:
                return True
            elif date < end:
                return True
        return false


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
    def checkWorkedHours(self,userId,controls):
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
