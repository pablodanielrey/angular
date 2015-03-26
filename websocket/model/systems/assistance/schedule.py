# -*- coding: utf-8 -*-
import psycopg2, inject
import datetime, pytz
import logging

from wexceptions import *

from model import utils
from model.systems.assistance.date import Date

class Schedule:

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

                st = schedule[0].time()
                se = schedule[1].time()

                """ retorno los schedules con la fecha actual en utc - las fechas en la base deberían estar en utc """
                schedules.append(
                    {
                        'start':date.replace(hour=st.hour,minute=st.minute,second=st.second,microsecond=st.microsecond),
                        'end':date.replace(hour=se.hour,minute=se.minute,second=se.second,microsecond=se.microsecond),
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
        chequea los schedules contra las horas trabajadas
        las fechas están en UTC y son aware
    """
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
                    """ no tiene schedule a controlar """
                    continue

                if wh is None or 'start' not in wh or 'end' not in wh:
                    """ no tiene nada trabajado!!! """
                    fails.append(
                        {
                            'date':date,
                            'description':'No existe ninguna marcación para esa fecha'
                        }
                    )
                    continue



                """ controlo la llegada """
                if wh['start'] is None:
                    fails.append(
                        {
                            'date': date,
                            'description':'Sin horario de llegada'
                        }
                    )

                elif wh['start'] > sched['start'] + tolerancia:
                    fails.append(
                        {
                            'date': date,
                            'description':'Llegada tardía',
                            'startSchedule':sched['start'],
                            'start':wh['start']
                        }
                    )


                """ controlo la salida """
                if wh['end'] is None:
                    fails.append(
                        {
                            'date': date,
                            'description':'Sin horario de salida'
                        }
                    )

                elif wh['end'] < sched['end'] - tolerancia:
                    fails.append(
                        {
                            'date': date,
                            'description':'Salida temprana',
                            'endSchedule':sched['end'],
                            'end':wh['end']
                        }
                    )

            return (userId,fails)
