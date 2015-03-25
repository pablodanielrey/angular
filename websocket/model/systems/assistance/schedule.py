# -*- coding: utf-8 -*-
import psycopg2, inject
import datetime, pytz

from wexceptions import *

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

        dateNow = self.date.utcNow()
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
                        'start':dateNow.replace(hour=st.hour,minute=st.minute,second=st.second,microsecond=st.microsecond),
                        'end':dateNow.replace(hour=se.hour,minute=se.minute,second=se.second,microsecond=se.microsecond),
                    }
                )

            else:
                break

        return schedules


    """
        chequea los logs contra lo que el usuario debería tener ese día
    """
    def checkSchedule(self,con,userId,logs):
        pass
        """
        fails = []

        for log in logs:
            start = log['start']
            end = log['end']
            date = start.date()
            schedules = self.getSchedule(con,userId,date)
            if start > schedules[0]['start']:
                fails.append({'schedule_start':,})
        """
