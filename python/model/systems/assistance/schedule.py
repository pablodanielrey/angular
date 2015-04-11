# -*- coding: utf-8 -*-
import psycopg2, inject
import datetime, pytz
import logging

from model.exceptions import *

from model import utils
from model.systems.assistance.date import Date
from model.systems.assistance.logs import Logs

class Schedule:

    logs = inject.attr(Logs)
    date = inject.attr(Date)

    """
        obtiene tods los schedules para un usuario en determinada fecha, solo deja los actuales, tiene en cuenta el historial ordenado por date
        la fecha esta en UTC
    """
    def getSchedule(self,con,userId,date):

        cur = con.cursor()
        cur.execute('set time zone %s',('utc',))

        """ obtengo todos los schedules que son en la fecha date del parámetro """
        cur.execute("select sstart, send, date from assistance.schedule where \
                    ((date = %s) or \
                    (isDayOfWeek = true and extract(dow from date) = extract(dow from %s)) or \
                    (isDayOfMonth = true and extract(day from date) = extract(day from %s)) or \
                    (isDayOfYear = true and extract(doy from date) = extract(doy from %s))) and \
                    user_id = %s \
                    order by date desc",(date,date,date,date,userId))
        scheduless = cur.fetchall()
        if scheduless is None or len(scheduless) <= 0:
            return []

        schedules = []

        if not self.date.isUTC(scheduless[0][2]):
            raise FailedConstraints('date in database not in UTC')

        dateS = scheduless[0][2].date()
        for schedule in scheduless:

            """ controlo que las fechas estén en utc """
            if not (self.date.isUTC(schedule[0]) and self.date.isUTC(schedule[1])):
                raise FailedConstraints('date in database not in UTC')

            if schedule[2].date() == dateS:

                sstart = schedule[0]
                zeroTime = sstart.replace(hour=0,minute=0,second=0,microsecond=0)
                initDelta = sstart - zeroTime
                endDelta = initDelta + (schedule[1] - sstart)

                actualZero = date.replace(hour=0,minute=0,second=0,microsecond=0)
                st = actualZero + initDelta
                se = actualZero + endDelta

                """ retorno los schedules con la fecha actual en utc - las fechas en la base deberían estar en utc """
                schedules.append(
                    {
                        'start':st,
                        'end':se
                    }
                )

            else:
                break

        return schedules


    """
        reotnra los ids de los usuarios que tiene algun contról de horario
    """
    def getUsersInSchedules(self,con):
        cur = con.cursor()
        cur.execute('select distinct user_id from assistance.schedule')
        if cur.rowcount <= 0:
            return []

        users = []
        for c in cur:
            users.append(c[0])
        return users


    """
        chequea el schedule de la fecha pasada como parámetro (se supone aware)
        los logs de agrupan por schedule, teniendo una tolerancia de 8 horas antes del siguiente schedule

    """
    def checkSchedule(self,con,userId,date):
        date = self.date.awareToUtc(date)

        schedules = self.getSchedule(con,userId,date)
        if schedules is None:
            return []

        if len(schedules) <= 0:
            return []

        schedules2 = []
        days = 1
        while schedules2 == None or len(schedules2) <= 0:
            date2 = date + datetime.timedelta(days=days)
            schedules2 = self.getSchedule(con,userId,date2)
            days = days + 1

        start2 = schedules2[0]['start']

        start = schedules[0]['start']
        end = schedules[-1]['end']

        logging.debug(schedules);

        logging.debug('start {} -- end {} '.format(start,end))

        deltaEnd = end + datetime.timedelta(seconds=((start2 - end).total_seconds() / 3))
        deltaStart = start - datetime.timedelta(hours=1)


        logging.debug('Chequeando fechas : {} -> {}'.format(deltaStart,deltaEnd))

        """
            obtengo los logs indicados para cubrir todo el schedule
        """
        logs = self.logs.findLogs(con,userId,deltaStart,deltaEnd)

        logging.debug(logs)

        whs,attlogs = self.logs.getWorkedHours(logs)
        controls = list(utils.combiner(schedules,whs))
        fails = self._checkScheduleWorkedHours(userId,controls)
        return fails




    """ chequea los schedules contra las workedhours calculadas """
    def _checkScheduleWorkedHours(self,userId,controls):
        tolerancia = datetime.timedelta(minutes=15)
        fails = []
        for sched,wh in controls:

            if sched is None:
                """ no tiene schedule a controlar """
                continue

            date = sched['start']

            if wh is None or 'start' not in wh or 'end' not in wh:
                """ no tiene nada trabajado!!! """
                fails.append(
                    {
                        'userId':userId,
                        'date':date,
                        'description':'No existe ninguna marcación para esa fecha'
                    }
                )
                continue



            """ controlo la llegada """
            if wh['start'] is None:
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Sin horario de llegada'
                    }
                )

            elif wh['start'] > sched['start'] + tolerancia:
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Llegada tardía',
                        'startSchedule':sched['start'],
                        'start':wh['start'],
                        'seconds':(wh['start'] - sched['start']).total_seconds()
                    }
                )


            """ controlo la salida """
            if wh['end'] is None:
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Sin horario de salida'
                    }
                )

            elif wh['end'] < sched['end'] - tolerancia:
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Salida temprana',
                        'endSchedule':sched['end'],
                        'end':wh['end'],
                        'seconds':(sched['end']-wh['end']).total_seconds()
                    }
                )

        return fails



    """
        chequea los schedules contra las horas trabajadas
        las fechas están en UTC y son aware
    def checkSchedule(self,con,userId,start,end,whs):

        #logging.debug('---------- check schedule ---------')
        #logging.debug('start : {0}, end: {1}'.format(start,end))
        #logging.debug('whs: {}'.format(whs))

        fails = []

        tolerancia = datetime.timedelta(minutes=15)

        delta = end - start
        dates = [ start ]
        for i in range(delta.days):
            dates.append(start + datetime.timedelta(days=i))

        for date in dates:

            #logging.debug('date: {}'.format(date))


            whsInDate = list(filter(lambda wh: wh['start'].date() == date.date(),whs))
            schedules = self.getSchedule(con,userId,date)
            controls = list(utils.combiner(schedules,whsInDate))

            date = self.date.localizeUtc(datetime.datetime.combine(date,datetime.time(0)))

            #logging.debug('whsInDate: {}'.format(whsInDate))
            #logging.debug('schedules: {}'.format(schedules))
            #logging.debug('controls: {}'.format(controls))

            for sched,wh in controls:

                if sched is None:
                    continue

                if wh is None or 'start' not in wh or 'end' not in wh:
                    fails.append(
                        {
                            'userId':userId,
                            'date':date,
                            'description':'No existe ninguna marcación para esa fecha'
                        }
                    )
                    continue


                if wh['start'] is None:
                    fails.append(
                        {
                            'userId':userId,
                            'date': date,
                            'description':'Sin horario de llegada'
                        }
                    )

                elif wh['start'] > sched['start'] + tolerancia:
                    fails.append(
                        {
                            'userId':userId,
                            'date': date,
                            'description':'Llegada tardía',
                            'startSchedule':sched['start'],
                            'start':wh['start'],
                            'minutes':wh['start'] - sched['start']
                        }
                    )


                if wh['end'] is None:
                    fails.append(
                        {
                            'userId':userId,
                            'date': date,
                            'description':'Sin horario de salida'
                        }
                    )

                elif wh['end'] < sched['end'] - tolerancia:
                    fails.append(
                        {
                            'userId':userId,
                            'date': date,
                            'description':'Salida temprana',
                            'endSchedule':sched['end'],
                            'end':wh['end'],
                            'minutes':sched['end']-wh['end']
                        }
                    )

            return (userId,fails)
    """
