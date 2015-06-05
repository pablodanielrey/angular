# -*- coding: utf-8 -*-
import psycopg2, inject, uuid
import datetime, pytz, calendar
import logging

from model.exceptions import *

from model import utils
from model.systems.assistance.date import Date
from model.systems.assistance.logs import Logs
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.justifications.justifications import Justifications


class ScheduleChecks:

    date = inject.attr(Date)
    schedule = inject.attr(Schedule)
    justifications = inject.attr(Justifications)
    logs = inject.attr(Logs)


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



    def _findJustificationsForDate(self,justifications,date):
        justs = []
        for j in justifications:
            logging.debug('chequeando fecha : {} == {}'.format(j['begin'].date(),date.date()))
            if j['begin'].date() == date.date():
                justs.append(j)
        return justs

    def _findGeneralJustificationsForDate(self,justifications,date):
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


        gjustifications = self.justifications.getGeneralJustificationRequests(con)
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
            scheds = self.schedule.getSchedule(con,userId,actualUtc)
            if (scheds is None) or (len(scheds) <= 0):
                """ no tiene horario declarado asi que no se chequea nada """
                actual = nextDay
                continue


            if check['type'] == 'PRESENCE':
                logging.debug('presencia {} {}'.format(userId,actualUtc))
                logs = self.schedule.getLogsForSchedule(con,userId,actualUtc)
                if (logs is None) or (len(logs) <= 0):
                    justs = self._findJustificationsForDate(justifications,actual)

                    gjusts = self._findGeneralJustificationsForDate(gjustifications,actual)
                    if len(gjusts) > 0:
                        for j in gjusts:
                            j['user_id'] = userId
                            justs.append(j)

                    fails.append(
                        {
                            'userId':userId,
                            'date':actual,
                            'description':'Sin marcación',
                            'justifications':justs
                        }
                    )


            elif check['type'] == 'HOURS':
                logs = self.schedule.getLogsForSchedule(con,userId,actualUtc)
                whs,attlogs = self.logs.getWorkedHours(logs)
                count = 0
                for wh in whs:
                    count = count + wh['seconds']

                if count < (check['hours'] * 60 * 60):

                    justs = self._findJustificationsForDate(justifications,actual)

                    gjusts = self._findGeneralJustificationsForDate(gjustifications,actual)
                    if len(gjusts) > 0:
                        for j in gjusts:
                            j['user_id'] = userId
                            justs.append(j)


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

                gjusts = self._findGeneralJustificationsForDate(gjustifications,actual)
                if len(gjusts) > 0:
                    for j in gjusts:
                        j['user_id'] = userId
                        justs.append(j)


                fail = self.checkSchedule(con,userId,actualUtc)
                for f in fail:
                    f['justifications'] = justs
                fails.extend(fail)

            actual = nextDay

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



    """
        chequea el schedule de la fecha pasada como parámetro (se supone aware)
        los logs de agrupan por schedule.
        teneiendo en cuenta la diferencia entre 2 schedules consecutivos dividido en 2.
    """
    def checkSchedule(self,con,userId,date):
        date = self.date.awareToUtc(date)

        schedules = self.schedule.getSchedule(con,userId,date)
        logs = self.schedule.getLogsForSchedule(con,userId,date)
        whs,attlogs = self.logs.getWorkedHours(logs)
        controls = list(utils.combiner(schedules,whs))
        fails = self._checkScheduleWorkedHours(userId,controls)
        return fails
