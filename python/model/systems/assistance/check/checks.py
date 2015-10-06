# -*- coding: utf-8 -*-
import psycopg2
import inject
import uuid
import datetime
import pytz
import calendar
import logging

from model.exceptions import *

from model import utils
from model.systems.assistance.date import Date
from model.systems.assistance.logs import Logs
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.justifications.justifications import Justifications

from model.systems.assistance.check.check import Check
from model.systems.assistance.check.scheduleCheck import ScheduleCheck
from model.systems.assistance.check.hoursCheck import HoursCheck
from model.systems.assistance.check.presenceCheck import PresenceCheck


class ScheduleChecks:

    date = inject.attr(Date)
    schedule = inject.attr(Schedule)
    justifications = inject.attr(Justifications)
    logs = inject.attr(Logs)

    scheduleCheck = ScheduleCheck()
    typesCheck = [scheduleCheck, HoursCheck(), PresenceCheck()]

    ''' retorna los chequeos que están programados dentro del código actual '''
    def getAvailableChecks(self):
        return self.typesCheck

    """
        retorna una lista cronológica de los chequeos a realizar para el usuario.
        en el caso del chequeo de horas retora la cantidad de horas a chequear.

        checks [
            {
                'id': id
                'start':fecha
                'end':fecha
                'type': 'NULL|PRESENCE|HOURS|SCHEDULE'
            }
        ]

    """
    def _getCheckData(self, con, userId, date):
        cur = con.cursor()
        cur.execute('select id,user_id,date,type,created from assistance.checks where user_id = %s order by date asc', (userId,))
        if cur.rowcount <= 0:
            return

        data = cur.fetchall()
        checks = []
        last = None
        current = None
        for c in data:

            for t in self.typesCheck:
                if t.isTypeCheck(c[3]):
                    current = t.create(c[0], c[1], c[2], cur)
                    break

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
    def getUsersWithChecks(self, con, date):
        cur = con.cursor()
        cur.execute('select distinct user_id from assistance.checks where date >= %s',(date,))
        if cur.rowcount <= 0:
            return []

        users = []
        for c in cur:
            users.append(c[0])
        return users


    def _findJustificationsForDate(self, justifications, date):
        justs = []
        for j in justifications:
            logging.debug('chequeando fecha : {} == {}'.format(j['begin'].date(), date.date()))
            if j['begin'].date() == date.date():
                justs.append(j)
        return justs

    def _findGeneralJustificationsForDate(self, justifications, date):
        justs = []
        for j in justifications:
            logging.debug('chequeando fecha : {} == {}'.format(j['begin'].date(), date.date()))
            if j['begin'].date() == date.date():
                justs.append(j)
        return justs

    """
        chequea la restricción del usuario entre determinadas fechas
        las fechas son aware.
    """
    def checkConstraints(self, con, userId, start, end):
        checks = self._getCheckData(con, userId, start)
        logging.debug('checks %s', (checks,))

        if (checks is None) or (len(checks) <= 0):
            return []

        gjustifications = self.justifications.getGeneralJustificationRequests(con)
        justifications = self.justifications.getJustificationRequestsByDate(con, status=['APPROVED'], users=[userId], start=start, end=end + datetime.timedelta(days=1))
        logging.debug('justificaciones encontradas : {} '.format(justifications))

        fails = []

        actual = start
        while actual <= end:

            """ elijo el check indicado para la fecha actual """
            check = None
            for c in checks:
                check = c
                if Check.isActualCheck(actual,c):
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

            justs = self._findJustificationsForDate(justifications,actual)

            gjusts = self._findGeneralJustificationsForDate(gjustifications,actual)
            if len(gjusts) > 0:
                for j in gjusts:
                    j['user_id'] = userId
                    justs.append(j)

            auxFails = []
            for tcheck in self.typesCheck:
                if tcheck.isTypeCheck(check["type"]):
                    auxFails = tcheck.getFails(self,userId,actual,con)
                    break

            if len(auxFails) > 0:
                fails.extend(auxFails)
            actual = nextDay

        return fails



    """ chequea los schedules contra las workedhours calculadas """
    '''
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
    '''

    """
        chequea el schedule de la fecha pasada como parámetro (se supone aware)
        los logs de agrupan por schedule.
        teneiendo en cuenta la diferencia entre 2 schedules consecutivos dividido en 2.

        controls = [{schdule:{},whs:[]}]
    """
    def checkSchedule(self, con, userId, date):

        date = self.date.awareToUtc(date)


        schedules = self.schedule.getSchedule(con, userId, date)
        logs = self.schedule.getLogsForSchedule(con, schedules, date)
        whs, attlogs = self.logs.getWorkedHours(logs)
        
        controls = self.schedule.combiner(schedules, whs)
    
        fails = self.scheduleCheck.checkWorkedHours(con,userId,controls)
        return fails
        
