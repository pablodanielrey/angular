# -*- coding: utf-8 -*-
import json
import base64
import logging
import inject
import psycopg2
import pytz
import dateutil.parser
from model.exceptions import *
from datetime import datetime, date, time, timedelta

from model.config import Config
from model.profiles import Profiles

from model.systems.assistance.assistance import Assistance
from model.systems.assistance.schedule import ScheduleData
import model.systems.assistance.date
from model.systems.assistance.fails import Fails
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.check.checks import ScheduleChecks
from model.systems.offices.offices import Offices
from model.systems.assistance.date import Date



import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession


class AssistanceWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.profiles = inject.instance(Profiles)
        self.assistance = inject.instance(Assistance)
        self.fails = inject.instance(Fails)
        self.dateutils = inject.instance(Date)
        self.checks = inject.instance(ScheduleChecks)

        self.date = inject.instance(model.systems.assistance.date.Date)
        self.offices = inject.instance(Offices)
        self.schedule = inject.instance(Schedule)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getFailsByDate_async, 'assistance.getFailsByDate')
        yield from self.register(self.getAssistanceStatusByDate_async, 'assistance.getAssistanceStatusByDate')
        yield from self.register(self.getAssistanceStatusByUsers_async, 'assistance.getAssistanceStatusByUsers')
        yield from self.register(self.getAssistanceData_async, 'assistance.getAssistanceData')
        yield from self.register(self.getUsersWithSchedules_async, 'assistance.getUsersWithSchedules')
        yield from self.register(self.getSchedules_async, 'assistance.getSchedules')
        yield from self.register(self.getSchedulesHistory_async, 'assistance.getSchedulesHistory')
        yield from self.register(self.persistSchedule_async, 'assistance.persistSchedule')
        yield from self.register(self.persistScheduleWeek_async, 'assistance.persistScheduleWeek')
        yield from self.register(self.deleteSchedule_async, 'assistance.deleteSchedule')
        yield from self.register(self.getAvailableChecks_async, 'assistance.getAvailableChecks')
        yield from self.register(self.getChecksByUser_async, 'assistance.getChecksByUser')
        yield from self.register(self.getUsersWithChecks_async, 'assistance.getUsersWithChecks')
        yield from self.register(self.getSchedulesByDate_async, 'assistance.getSchedulesByDate')
        yield from self.register(self.getLogsForSchedulesByDate_async, 'assistance.getLogsForSchedulesByDate')




    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def _parseDate(self, date):
        return self.date.parse(date)

    def _parseDates(self, dates):
        ds = []
        for d in dates:
            ds.append(self.date.parse(d))
        return ds

    def getAssistanceData(self, sid, userId, date=None):
        con = self._getDatabase()
        try:
            if date is not None:
                date = self._parseDate(date)

            r = self.assistance.getAssistanceData(con, userId, date)
            scheds = r['schedule']
            schedsMap = []
            for s in scheds:
                schedsMap.append(s.toMap(date))
            r['schedule'] = schedsMap
            return r

        finally:
            con.close()

    @coroutine
    def getAssistanceData_async(self, sid, userId, date=None):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getAssistanceData, sid, userId, date)
        return r

    def getAssistanceStatusByDate(self, userId, date=None):
        con = self._getDatabase()
        try:
            if date is not None:
                date = self._parseDate(date)
            r = self.assistance.getAssistanceStatus(con, userId, date)
            return r

        finally:
            con.close()

    @coroutine
    def getAssistanceStatusByDate_async(self, sid, userId, date=None):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getAssistanceStatusByDate, userId, date)
        return r

    def getAssistanceStatusByUsers(self, sid, userIds, dates,status):
        logging.debug(dates)
        con = self._getDatabase()
        try:
            if dates is not None:
                dates = self._parseDates(dates)
            st = self.assistance.getAssistanceStatusByUsers(con, userIds, dates,status)
            b64 = self.assistance.arrangeAssistanceStatusByUsers(con,st)
            ret = {'base64':b64,'assistances':st}
            return ret

        finally:
            con.close()

    @coroutine
    def getAssistanceStatusByUsers_async(self, sid, userIds, dates,status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getAssistanceStatusByUsers, sid, userIds, dates, status)
        return r

    def getUsersWithSchedules(self, sid):
        con = self._getDatabase()
        try:
            r = self.schedule.getUsersInSchedules(con)
            return r

        finally:
            con.close()

    @coroutine
    def getUsersWithSchedules_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getUsersWithSchedules, sid)
        return r

    def getSchedules(self, sid, userId, date):
        con = self._getDatabase()
        try:
            if date is None:
                return None;

            date = self._parseDate(date)
            scheds = self.schedule.getSchedulesOfWeek(con, userId, date)

            schedsMap = []

            weekday = datetime.weekday(date)
            date -= timedelta(days=weekday)
            for s in scheds:
                weekday = datetime.weekday(s.date)
                d = date + timedelta(days=weekday)
                schedsMap.append(s.toMap(d))
            return schedsMap

        finally:
            con.close()

    @coroutine
    def getSchedules_async(self, sid, userId, date):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getSchedules, sid, userId, date)
        return r

    def getSchedulesHistory(self, sid, userId):
        con = self._getDatabase()
        try:
            scheds = self.schedule.getSchedulesHistory(con, userId)
            schedsMap = []
            for s in scheds:
                date = s.date
                schedsMap.append(s.toMap(date))
            return schedsMap

        finally:
            con.close()
    @coroutine
    def getSchedulesHistory_async(self, sid, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getSchedulesHistory, sid, userId)
        return r

    def persistSchedule(self, sid, userId, date, start, end, dayOfWeek=False, dayOfMonth=False, dayOfYear=False):
        con = self._getDatabase()
        try:
            date = self._parseDate(date)
            r = self.schedule.persistSchedule(con, userId, date, start, end, dayOfWeek, dayOfMonth, dayOfYear)
            con.commit()
            return r

        finally:
            con.close()

    @coroutine
    def persistSchedule_async(self, sid, userId, date, start, end, dayOfWeek=False, dayOfMonth=False, dayOfYear=False):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistSchedule, sid, userId, date, start, end, dayOfWeek, dayOfMonth, dayOfYear)
        return r


    def persistScheduleWeek(self, sid, userId, date, start, end, daysOfWeek):
        con = self._getDatabase()
        try:
            date = self._parseDate(date)
            r = self.schedule.persistScheduleWeek(con, userId, date, start, end, daysOfWeek)
            con.commit()
            return r

        finally:
            con.close()

    @coroutine
    def persistScheduleWeek_async(self, sid, userId, date, start, end, daysOfWeek):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistScheduleWeek, sid, userId, date, start, end, daysOfWeek)
        return r

    def deleteSchedule(self, sid, id):
        con = self._getDatabase()
        try:
            self.schedule.deleteSchedule(con, id)
            con.commit()
            return True

        except Exception as e:
            logging.exception(e)
            return False

        finally:
            con.close()

    @coroutine
    def deleteSchedule_async(self, sid, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.deleteSchedule, sid, id)
        return r

    def getAvailableChecks(self, sid):
        con = self._getDatabase()
        try:
            r = self.checks.getAvailableChecks()
            cs = []
            for c in r:
                cs.append(type(c).__name__)
            return cs

        finally:
            con.close()

    @coroutine
    def getAvailableChecks_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getAvailableChecks, sid)
        return r

    def getChecksByUser(self, sid, userId, date):
        """
           obtener checks de un usuario a partir de cierta fecha
           @param sid Identificacion de Session
           @param userId Identificacion de usuario
           @param date String con la fecha, en formato "Y-m-d", por ejemplo "2000-12-31"
        """
        date = self.date.parse(date).date()

        con = self._getDatabase()
        try:
            cs = self.checks._getCheckData(con, userId, date)
            logging.debug(cs)
            return cs

        finally:
            con.close()

    @coroutine
    def getChecksByUser_async(self, sid, userId, date):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getChecksByUser, sid, userId, date)
        return r


    def getUsersWithChecks(self, sid, date):
        con = self._getDatabase()
        try:
            cs = self.checks.getUsersWithChecks(con, date)
            return cs

        finally:
            con.close()

    @coroutine
    def getUsersWithChecks_async(self, sid, date):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getUsersWithChecks, sid, date)
        return r


    def getFailsByDate(self, sid, userId, start, end):
        start = dateutil.parser.parse(start).date()
        end = dateutil.parser.parse(end).date()

        con = self._getDatabase()
        try:
            r = self.assistance.getFailsByDate(con, userId, start, end)
            return r

        finally:
            con.close()

    @coroutine
    def getFailsByDate_async(self, sid, userId, start, end):

        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getFailsByDate, sid, userId, start, end)
        return r



    def getSchedulesByDate(self, userId, date):
        """
         " Obtener schedules de una fecha determinada
         " @param userId Id de usuario al cual se le va a pedir los schedules
         " @param date Fecha para la cual se quieren consultar los schedules
         """

        date = datetime.strptime(date, "%Y-%m-%d").date()

        con = self._getDatabase()
        try:
            schedulesData = self.schedule.getSchedule(con, userId, date)

            schedules = []
            for schData in schedulesData:

              sch = {
                "id":schData.id,
                "date":schData.date,
                "start":schData.start,
                "end":schData.end,
                "date":schData.date,
                "isDayOfWeek":schData.isDayOfWeek,
                "isDayOfMonth":schData.isDayOfMonth,
                "isDayOfYear":schData.isDayOfYear,
                "previousDate":schData.previousDate,
                "nextDate":schData.nextDate,
                "userId":schData.userId,

              }
              schedules.append(sch)

            return schedules

        finally:
            con.close()

    @coroutine
    def getSchedulesByDate_async(self, userId, date):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getSchedulesByDate, userId, date)
        return r



    def getLogsForSchedulesByDate(self, schedules, date):
        """
         " Obtener schedules de una fecha determinada
         " @param schedules Lista de diccionario con los datos de los schedules del usuario al cual se le solicitaran los logs
         """

        date = datetime.strptime(date, "%Y-%m-%d").date()
        con = self._getDatabase()
        try:
            schedulesData = []
            for schedule in schedules:
                dateSch = datetime.strptime(schedule["date"], "%Y-%m-%d").date()

                sch = {
                  'id': schedule["id"],
                  'date': dateSch,
                  'start': schedule["start"],
                  'end': schedule["end"],
                  'isDayOfWeek': schedule["isDayOfWeek"],
                  'isDayOfMonth': schedule["isDayOfMonth"],
                  'isDayOfYear': schedule["isDayOfYear"],
                  'userId': schedule["userId"]
                }
                schData = ScheduleData(sch, self.date.getLocalTimezone())

                schedulesData.append(schData)

            logs = self.schedule.getLogsForSchedule(con, schedulesData, date)
            return logs

        finally:
            con.close()

    @coroutine
    def getLogsForSchedulesByDate_async(self, schedules, date):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getLogsForSchedulesByDate, schedules, date)
        return r
