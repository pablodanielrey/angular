# -*- coding: utf-8 -*-
import psycopg2, inject
import datetime, pytz
import logging

from model.exceptions import *

from model import utils
from model.systems.assistance.date import Date
from model.systems.assistance.logs import Logs
from model.systems.assistance.justifications.justifications import Justifications

class Schedule:

    logs = inject.attr(Logs)
    date = inject.attr(Date)
    justifications = inject.attr(Justifications)



    """
        retorna una lista cronológica de los chequeos a realizar para el usuario.
        en el caso del chequeo de horas retora la cantidad de horas a chequear.

        checks [
            {
                'start':fecha
                'end':fecha
                'type': 'NULL|PRESENCE|HOURS|SCHEDULE'
            }
        ]

    """
    def _getCheckData(self,con,userId):
        cur = con.cursor()
        cur.execute('select id,user_id,date,type,created from assistance.checks where user_id = %s order by date asc',(userId,))
        if cur.rowcount <= 0:
            return

        data = cur.fetchall()
        checks = []
        last = None
        current = None
        for c in data:
            current = {
                'start':c[2],
                'end':None,
                'type':c[3]
            }

            if current['type'] == 'HOURS':
                cur.execute('select hours from assistance.hours_check where id = %s',(c[0],))
                h = cur.fetchone()
                current['hours'] = h[0]

            if last is not None:
                last['end'] = current['start']
                checks.append(last)
            last = current

        if last is not None:
            checks.append(last)

        return checks


    """
        Retorna la lista de logs determinada que debería tener un usuario para una fecha específica,
        se tiene en cuenta el horario de la persona en la fecha y la fecha siguiente para obtener los logs correctos.
    """
    def _getLogsForSchedule(self,con,userId,date):

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

        deltaEnd = end + datetime.timedelta(seconds=((start2 - end).total_seconds() / 2))
        deltaStart = start - datetime.timedelta(hours=1)

        logs = self.logs.findLogs(con,userId,deltaStart,deltaEnd)

        return logs





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
        obtiene tods los schedules para un usuario, incluyendo el historial
    """
    def getScheduleHistory(self,con,userId):

        cur = con.cursor()
        cur.execute('set time zone %s',('utc',))

        """ obtengo todos los schedules"""
        cur.execute("select sstart, send, date, isDayOfWeek, isDayOfMonth, isDayOfYear from assistance.schedule where \
                    user_id = %s \
                    order by date desc",(userId,))
        scheduless = cur.fetchall()
        if scheduless is None or len(scheduless) <= 0:
            return []

        schedules = []

        if not self.date.isUTC(scheduless[0][2]):
            raise FailedConstraints('date in database not in UTC')

        for schedule in scheduless:

            """ controlo que las fechas estén en utc """
            if not (self.date.isUTC(schedule[0]) and self.date.isUTC(schedule[1])):
                raise FailedConstraints('date in database not in UTC')


            """ retorno los schedules con la fecha actual en utc - las fechas en la base deberían estar en utc """
            schedules.append(
                {
                    'start':schedule[0],
                    'end':schedule[1],
                    'isDayOfWeek':schedule[3],
                    'isDayOfMonth':schedule[4],
                    'isDayOfYear':schedule[5]
                }
            )


        return schedules


    """
        obtiene los usuarios que tienen configurado algún chequeo
    """
    def getUsersWithConstraints(self,con):
        cur = con.cursor()
        cur.execute('select distinct user_id from assistance.checks')
        if cur.rowcount <= 0:
            return []

        users = []
        for c in cur:
            users.append(c[0])
        return users



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



    def _findJustificationsForDate(self,justifications,date):
        justs = []
        for j in justifications:
            logging.debug('chequeando fecha : {} == {}'.format(j['begin'].date(),date.date()))
            if j['begin'].date() == date.date():
                justs.append(j)
        return justs


    """
        chequea la restricción del usuario entre determinadas fechas
        las fechas son aware.
    """
    def checkConstraints(self,con,userId,start,end):
        checks = self._getCheckData(con,userId)
        logging.debug('checks %s',(checks,))

        if (checks is None) or (len(checks) <= 0):
            return []


        justifications = self.justifications.getJustificationRequestsByDate(con,status=['APPROVED'],users=[userId],start=start,end=end + datetime.timedelta(days=1))
        logging.debug('justificaciones encontradas : {} '.format(justifications))

        fails = []

        actual = start
        while actual <= end:

            """ elijo el check indicado para la fecha actual """
            check = None
            for c in checks:
                check = c
                if (actual >= c['start']):
                    if c['end'] is None:
                        check = c
                        break
                    elif actual < c['end']:
                        check = c
                        break

            nextDay = actual + datetime.timedelta(days=1)

            if check is None:
                actual = nextDay
                continue

            actualUtc = self.date.awareToUtc(actual)
            scheds = self.getSchedule(con,userId,actualUtc)
            if (scheds is None) or (len(scheds) <= 0):
                """ no tiene horario declarado asi que no se chequea nada """
                actual = nextDay
                continue


            if check['type'] == 'PRESENCE':
                logging.debug('presencia {} {}'.format(userId,actualUtc))
                logs = self._getLogsForSchedule(con,userId,actualUtc)
                if (logs is None) or (len(logs) <= 0):
                    justs = self._findJustificationsForDate(justifications,actual)
                    fails.append(
                        {
                            'userId':userId,
                            'date':actual,
                            'description':'Sin marcación',
                            'justifications':justs
                        }
                    )


            elif check['type'] == 'HOURS':
                logs = self._getLogsForSchedule(con,userId,actualUtc)
                whs,attlogs = self.logs.getWorkedHours(logs)
                count = 0
                for wh in whs:
                    count = count + wh['seconds']

                if count < (check['hours'] * 60 * 60):

                    justs = self._findJustificationsForDate(justifications,actual)
                    fails.append(
                        {
                            'userId':userId,
                            'date':actual,
                            'description':'No trabajó la cantidad mínima de minutos requeridos ({} < {})'.format(count / 60, check['hours'] * 60),
                            'justifications':justs
                        }
                    )

            elif check['type'] == 'SCHEDULE':
                justs = self._findJustificationsForDate(justifications,actual)
                fail = self.checkSchedule(con,userId,actualUtc)
                for f in fail:
                    f['justifications'] = justs
                fails.extend(fail)

            actual = nextDay

        return fails




    """
        chequea el schedule de la fecha pasada como parámetro (se supone aware)
        los logs de agrupan por schedule.
        teneiendo en cuenta la diferencia entre 2 schedules consecutivos dividido en 2.
    """
    def checkSchedule(self,con,userId,date):
        date = self.date.awareToUtc(date)

        schedules = self.getSchedule(con,userId,date)
        logs = self._getLogsForSchedule(con,userId,date)
        whs,attlogs = self.logs.getWorkedHours(logs)
        controls = list(utils.combiner(schedules,whs))
        fails = self._checkScheduleWorkedHours(userId,controls)
        return fails




    """ chequea los schedules contra las workedhours calculadas """
    def _checkScheduleWorkedHours(self,userId,controls):
        tolerancia = datetime.timedelta(minutes=16)
        fails = []

        for sched,wh in controls:

            if sched is None:
                """ no tiene schedule a controlar """
                continue

            date = sched['start']

            if (wh is None) or ('start' not in wh and 'end' not in wh):
                """ no tiene nada trabajado!!! """
                fails.append(
                    {
                        'userId':userId,
                        'date':date,
                        'description':'Sin marcación'
                    }
                )
                continue



            """ controlo la llegada """
            if wh['start'] is None:
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Sin entrada'
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
                        'seconds':(wh['start'] - sched['start']).total_seconds(),
                        'whSeconds':wh['seconds']
                    }
                )


            """ controlo la salida """
            if wh['end'] is None:
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Sin salida'
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
                        'seconds':(sched['end']-wh['end']).total_seconds(),
                        'whSeconds':wh['seconds']
                    }
                )

        return fails
