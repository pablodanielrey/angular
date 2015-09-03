# -*- coding: utf-8 -*-
import sys
import base64
import psycopg2
import datetime
import logging
import uuid
import inject
import datetime
import itertools
from collections import OrderedDict
import io
from pyexcel_ods3 import ODSWriter

from model.utils import DateTimeEncoder
from model.config import Config
from model.users.users import Users

from model.systems.assistance.fails import Fails
from model.systems.assistance.logs import Logs
from model.systems.assistance.date import Date
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.check.checks import ScheduleChecks
from model.systems.assistance.justifications.justifications import Justifications
from model.systems.positions.positions import Positions
import model.systems.assistance.date


class Assistance:

    config = inject.attr(Config)
    date = inject.attr(Date)
    logs = inject.attr(Logs)
    schedule = inject.attr(Schedule)
    users = inject.attr(Users)
    justifications = inject.attr(Justifications)
    checks = inject.attr(ScheduleChecks)
    positions = inject.attr(Positions)
    date = inject.attr(model.systems.assistance.date.Date)

    def getAssistanceData(self, con, userId, date=None):
        ps = self.positions.find(con, userId)
        p = ''
        if len(ps) > 0:
            p = ps[0]['name']

        if date is None:
            date = datetime.datetime.now()
        if self.date.isNaive(date):
            ldate = self.date.localizeLocal(date)
            date = self.date.awareToUtc(ldate)

        sch = self.schedule.getSchedule(con, userId, date)

        rt = {
            'userId': userId,
            'schedule': sch,
            'position': p
        }
        return rt

    def _resolveJustificationsNames(self, con, justifications):
        for j in justifications:
            jid = j['justification_id']
            j['name'] = self.justifications.getJustificationById(con, jid)['name']

    def _getJustificationsForSchedule(self, con, userId, scheds):
        if scheds is None or len(scheds) <= 0:
            return []

        start = scheds[0]['start']
        end = scheds[-1]['end']
        justifications = self.justifications.getJustificationRequestsByDate(con, None, [userId], start, end)
        self._resolveJustificationsNames(con, justifications)
        return justifications

    """
        Obtiene el estado de asistencia del usuario
        IMPORANTE!!!
        la fecha se toma como aware y en zona local del cliente!!!
        se pasa a utc dentro de este método ya que se necesita saber el inicio del día y fin del día en zona local.
    """
    def getAssistanceStatus(self, con, userId, date=None):

        if date is None:
            date = datetime.datetime.now()
        if self.date.isNaive(date):
            date = self.date.localizeLocal(date)

        # Chequeo que tenga horario
        scheds = self.schedule.getSchedule(con, userId, date)
        if (scheds is None) or (len(scheds) <= 0):
            """ no tiene horario declarado asi que no se chequea nada """
            return None

        logs = self.schedule.getLogsForSchedule(con, userId, scheds)
        logging.debug('logs {}'.format(logs))

        worked, attlogs = self.logs.getWorkedHours(logs)
        logging.debug('worked : {}, attlogs: {}'.format(worked, attlogs))

        sdate, edate, totalSeconds = self.logs.explainWorkedHours(worked)
        inside = 'Afuera' if len(attlogs) % 2 == 0 else 'Trabajando'

        justifications = self._getJustificationsForSchedule(con, userId, scheds)

        assistanceStatus = {
            'date': date,
            'userId': userId,
            'status': inside,
            'start': sdate,
            'end': edate,
            'logs': attlogs,
            'justifications': justifications,
            'schedules': scheds,
            'workedMinutes': totalSeconds / 60
        }
        return assistanceStatus

    def _getNullAssistanceStatus(self, con, userId, date):
        scheds = self.schedule.getSchedule(con, userId, date)
        justifications = self._getJustificationsForSchedule(con, userId, scheds)
        assistanceStatus = {
            'date': date,
            'userId': userId,
            'status': 'Afuera',
            'start': None,
            'end': None,
            'logs': [],
            'justifications': justifications,
            'schedules': scheds,
            'workedMinutes': 0
        }
        return assistanceStatus

    def getAssistanceStatusByUsers(self, con, usersIds, dates):
        statuses = {}
        for userId in usersIds:
            sts = []
            for date in dates:
                st = self.getAssistanceStatus(con, userId, date)
                if st is not None:
                    sts.append(st)
                else:
                    st = self._getNullAssistanceStatus(con, userId, date)
                    sts.append(st)
            statuses[userId] = sts
        return statuses

    """
        ////////////////////////////////////////// chequeo del tema de incumplimientos ////////////////////
    """


    def _arrangeForOdsChecks(self, con, data):

        values = [['Fecha','Dni','Nombre','Apellido','Hora Declarada','Hora de Marcación','Diferencia','Descripción','Horas Trabajadas','Justificación']]
        for l in data:
            v = []

            userId = l['userId']
            user = self.users.findUser(con,userId)

            v.append(l['date'].astimezone(tz=None).date())
            v.append(user['dni'])
            v.append(user['name'])
            v.append(user['lastname'])

            if 'startSchedule' in l:
                v.append(l['startSchedule'].astimezone(tz=None).time())
            elif 'endSchedule' in l:
                v.append(l['endSchedule'].astimezone(tz=None).time())
            else:
                v.append('')


            if 'start' in l:
                v.append(l['start'].astimezone(tz=None).time())
            elif 'end' in l:
                v.append(l['end'].astimezone(tz=None).time())
            else:
                v.append('')


            if 'seconds' in l:
                v.append('{:02d}:{:02d}'.format(int(l['seconds'] / 60 / 60), int(l['seconds'] / 60 % 60)))
            else:
                v.append('')


            v.append(l['description'])


            if 'whSeconds' in l:
                v.append('{:02d}:{:02d}'.format(int(l['whSeconds'] / 60 / 60), int(l['whSeconds'] / 60 % 60)))
            else:
                v.append('')



            if 'justifications' in l:
                self._resolveJustificationsNames(con,l['justifications'])
                for j in l['justifications']:
                    v.append(j['name'])
            else:
                v.append('')

            values.append(v)

        return values


    def arrangeCheckSchedule(self, con, data):
        odata = self._arrangeForOdsChecks(con,data)
        return self._exportToOds(odata)




    """
        chequea el schedule de los usuarios pasados como parametro.
        las fechas start y end son aware
    """
    def checkSchedule(self, userIds, start, end):

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            if self.date.isNaive(start):
                start = self.date.localizeLocal(start)
            elif self.date.isUTC(start):
                start = self.date.localizeAwareToLocal(start)

            if self.date.isNaive(end):
                end = self.date.localizeLocal(end)
            elif self.date.isUTC(end):
                end = self.date.localizeAwareToLocal(end)

            schedulesFails = []
            users = []
            for u in userIds:
                logging.debug('chequeando usuario %s',(u,))
                users.append(self.users.findUser(con,u))
                schedulesFails.extend(self.checks.checkConstraints(con,u,start,end))

            return (users,schedulesFails)

        finally:
            con.close()
