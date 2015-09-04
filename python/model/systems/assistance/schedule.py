# -*- coding: utf-8 -*-
import psycopg2, inject, uuid
import datetime, pytz, calendar
import logging

from model.exceptions import *

from model import utils
from model.systems.assistance.date import Date
from model.systems.assistance.logs import Logs


class Schedule:

    logs = inject.attr(Logs)
    date = inject.attr(Date)

    """
        Retorna la lista de logs determinada que deber�a tener un usuario para una fecha espec�fica,
        se tiene en cuenta el horario de la persona en la fecha y la fecha siguiente para obtener los logs correctos.
    """
    def getLogsForSchedule(self, con, userId, schedules):

        if schedules is None:
            return []

        if len(schedules) <= 0:
            return []

        start = schedules[0]['start']
        end = schedules[-1]['end']

        count = 0
        schedules2 = []
        days = 1
        while (count < 10) and (schedules2 is None or len(schedules2) <= 0):
            date2 = start + datetime.timedelta(days=days)
            schedules2 = self.getSchedule(con, userId, date2)
            days = days + 1
            count = count + 1

        if schedules2 is None or len(schedules2) <= 0:
            start2 = end + datetime.timedelta(hours=24)
        else:
            start2 = schedules2[0]['start']

        """
        schedules2 = []
        days = 1
        count = 0
        while (count < 10) or (schedules2 is None or len(schedules2) <= 0):
            date2 = date - datetime.timedelta(days=days)
            schedules2 = self.getSchedule(con,userId,date2)
            days = days + 1
            count = count + 1

        if schedules2 is None or len(schedules2) <= 0:
            end2 = start - datetime.timedelta(hours=24)
        else:
            end2 = schedules2[0]['end']
        """

        deltaEnd = end + datetime.timedelta(seconds=((start2 - end).total_seconds() / 2))
        """
        deltaStart = start - datetime.timedelta(seconds=((start - end2).total_seconds() / 2))
        """
        deltaStart = start - datetime.timedelta(hours=3)

        logs = self.logs.findLogs(con, userId, deltaStart, deltaEnd)

        return logs

    """
        obtiene tods los schedules para un usuario en determinada fecha, solo deja los actuales, tiene en cuenta el historial ordenado por date
        la fecha esta en UTC
    """
    def getSchedule(self, con, userId, date):
        if self.date.isNaive(date):
            raise Exception('date is naive')

        date = self.date.awareToUtc(date)   # trabajo con las fechas en utc
        cur = con.cursor()
        cur.execute('set time zone %s', ('utc',))

        """ obtengo todos los schedules que son en la fecha date del parámetro """
        cur.execute("select sstart, send, date, id from assistance.schedule where \
                    ((date = %s) or \
                    (isDayOfWeek = true and date <= %s and extract(dow from date) = extract(dow from %s)) or \
                    (isDayOfMonth = true and date <= %s and extract(day from date) = extract(day from %s)) or \
                    (isDayOfYear = true and date <= %s and extract(doy from date) = extract(doy from %s))) and \
                    user_id = %s \
                    order by date desc", (date, date, date, date, date, date, date, userId))
        scheduless = cur.fetchall()
        if scheduless is None or len(scheduless) <= 0:
            return []

        schedules = []

        if not self.date.isUTC(scheduless[0][2]):
            raise FailedConstraints('date in database not in UTC')

        dateS = scheduless[0][2].date()
        for schedule in scheduless:

            """ controlo que las fechas están en utc """
            if not (self.date.isUTC(schedule[0]) and self.date.isUTC(schedule[1])):
                raise FailedConstraints('date in database not in UTC')

            if schedule[2].date() == dateS:

                sstart = schedule[0]
                zeroTime = sstart.replace(hour=0, minute=0, second=0, microsecond=0)
                initDelta = sstart - zeroTime
                endDelta = initDelta + (schedule[1] - sstart)

                actualZero = date.replace(hour=0, minute=0, second=0, microsecond=0)
                st = actualZero + initDelta
                se = actualZero + endDelta

                """ me aseguro de que las fechas tengan si o si un timezone """
                assert st.tzinfo is not None
                assert se.tzinfo is not None

                """ retorno los schedules con la fecha actual en utc - las fechas en la base deber�an estar en utc """
                schedules.append(
                    {
                        'start': st,
                        'end': se,
                        'id': schedule[3]
                    }
                )

            else:
                break

        # ordeno los schedules por el start
        schedules = sorted(schedules, key=lambda schedule: schedule['start'])

        return schedules

    """
        obtiene todos los schedules para un usuario
    """
    def getSchedulesHistory(self, con, userId):
        cur = con.cursor()
        cur.execute('set time zone %s', ('utc',))

        cur.execute("select sstart, send, date, isDayOfWeek, isDayOfMonth, isDayOfYear, id from assistance.schedule where \
                user_id = %s \
                order by date desc", (userId,))
        scheduless = cur.fetchall()
        if scheduless is None or len(scheduless) <= 0:
            return []

        schedules = []

        if not self.date.isUTC(scheduless[0][2]):
            raise FailedConstraints('date in database not in UTC')

        for schedule in scheduless:

            """ controlo que las fechas est�n en utc """
            if not (self.date.isUTC(schedule[0]) and self.date.isUTC(schedule[1])):
                raise FailedConstraints('date in database not in UTC')

            """ retorno los schedules con la fecha actual en utc - las fechas en la base deber�an estar en utc """
            schedules.append(
                {
                    'id': schedule[6],
                    'start': schedule[0],
                    'end': schedule[1],
                    'date': schedule[2],
                    'isDayOfWeek': schedule[3],
                    'isDayOfMonth': schedule[4],
                    'isDayOfYear': schedule[5]
                }
            )

        return schedules

    """
        obtiene los schedules de la semana pasada en el date para un usuario
    """
    def getSchedulesOfWeek(self,con,userId,date):

        if date is None:
            date = self.date.now()
            date = date.replace(hour=0,minute=0,second=0,microsecond=0)

        # paso la fecha a utc
        date = self.date.awareToUtc(date)

        # obtengo el primer dia de la semana del date (L-0 .. D-6)
        weekday = datetime.date.weekday(date)
        date -= datetime.timedelta(days=weekday)

        schedules = []

        for x in range(0, 7):
            sch = self.getSchedule(con,userId,date)
            schedules.append(sch)
            date += datetime.timedelta(days=1)

        return schedules


    """
        reotnra los ids de los usuarios que tiene algun contr�l de horario
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
        genera un nuevo schedule las fechas pasadas como par�metro (se supone aware)
    """
    def newSchedule(self,con,userId,date,start,end,isDayOfWeek,isDayOfMonth,isDayOfYear):
        uaware = date.astimezone(pytz.utc)
        ustart = start.astimezone(pytz.utc)
        uend = end.astimezone(pytz.utc)

        cur = con.cursor()
        cur.execute('set time zone %s',('utc',))

        req = (str(uuid.uuid4()), userId, uaware, ustart, uend, isDayOfWeek, isDayOfMonth, isDayOfYear)
        cur.execute('insert into assistance.schedule (id,user_id,date,sstart,send,isDayOfWeek,isDayOfMonth,isDayOfYear) values (%s,%s,%s,%s,%s,%s,%s,%s)',req)

    '''
        elimina un schedule
    '''
    def deleteSchedule(self,con,id):
        cur = con.cursor()
        cur.execute('delete from assistance.schedule where id = %s',(id,))

    '''
        combina los whs con los schedules
        retorna [{schdule:{},whs:[]}]
    '''
    def combiner(self,schedules,whs):
        controls = []

        if schedules is None or len(schedules) == 0:
            return controls

        # ordeno los schedules y los whs por horario ascendente
        schedules = sorted(schedules, key=lambda schedule: schedule['start'])
        whs = sorted(whs, key=lambda wh: wh['start'])

        for sched in schedules:
            elem = {'schedule':sched,'whs':[]}
            if len(schedules) == 1:
                elem['whs'].extend(whs)
                whsAppends = whs
            else:
                whsAppends = []
                for wh in whs:
                    if 'start' in wh and wh['start'] <= sched['end']:
                        elem['whs'].append(wh)
                        whsAppends.append(wh)

                for w in whsAppends:
                    whs.remove(w)

            controls.append(elem)

        return controls
