# -*- coding: utf-8 -*-
import json
import base64
import logging
import inject
import psycopg2
import pytz
import datetime
import dateutil.parser
from model.exceptions import *

from model.config import Config
from model.profiles import Profiles

from model.systems.assistance.assistance import Assistance
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

        self.assistance = inject.instance(Assistance)
        self.date = inject.instance(model.systems.assistance.date.Date)
        self.offices = inject.instance(Offices)
        self.schedule = inject.instance(Schedule)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getFailsByDate_async, 'assistance.getFailsByDate')
        yield from self.register(self.getFailsByFilter_async, 'assistance.getFailsByFilter')
        yield from self.register(self.getAssistanceStatusByDate_async, 'assistance.getAssistanceStatusByDate')
        yield from self.register(self.getAssistanceStatusByUsers_async, 'assistance.getAssistanceStatusByUsers')
        yield from self.register(self.getAssistanceData_async, 'assistance.getAssistanceData')
        yield from self.register(self.getUsersWithSchedules_async, 'assistance.getUsersWithSchedules')
        yield from self.register(self.getSchedules_async, 'assistance.getSchedules')
        yield from self.register(self.persistSchedule_async, 'assistance.persistSchedule')
        yield from self.register(self.deleteSchedule_async, 'assistance.deleteSchedule')

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
            r = self.assistance.getAssistanceData(con, userId, date)
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

    def getAssistanceStatusByUsers(self, sid, userIds, dates):
        logging.debug(dates)
        con = self._getDatabase()
        try:
            if dates is not None:
                dates = self._parseDates(dates)
            st = self.assistance.getAssistanceStatusByUsers(con, userIds, dates)
            con.commit()
            return st

        finally:
            con.close()

    @coroutine
    def getAssistanceStatusByUsers_async(self, sid, userIds, dates):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getAssistanceStatusByUsers, sid, userIds, dates)
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
            date = self._parseDate(date)
            r = self.schedule.getSchedule(con, userId, date)
            return r

        finally:
            con.close()

    @coroutine
    def getSchedules_async(self, sid, userId, date):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getSchedules, sid, userId, date)
        return r

    def persistSchedule(self, sid, userId, date, start, end, dayOfWeek=False, dayOfMonth=False, dayOfYear=False):
        con = self._getDatabase()
        try:
            date = self._parseDate(date)
            start = self._parseDate(start)
            end = self._parseDate(end)
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

    def getFailsByDate(self, start, end):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getFailsByDate_async(self, sid, start, end):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getFailsByDate, start, end)
        return r






    def getFailsByFilter(self, userIds, officesIds, start, end, filter):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getFailsByFilter_async(self, sid, userIds, officesIds, start, end, filter):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getFailsByFilter, userIds, officesIds, start, end, filter)
        return r
