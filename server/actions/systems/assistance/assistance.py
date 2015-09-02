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
        self.profiles = inject.attr(Profiles)
        self.config = inject.attr(Config)
        self.assistance = inject.attr(Assistance)
        self.fails = inject.attr(Fails)
        self.dateutils = inject.attr(Date)
        self.checks = inject.attr(ScheduleChecks)

        self.offices = inject.attr(Offices)
        self.schedule = inject.attr(Schedule)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getFailsByDate_async, 'assistance.getFailsByDate')
        yield from self.register(self.getFailsByFilter_async, 'assistance.getFailsByFilter')
        yield from self.register(self.getAssistanceStatusByDate_async, 'assistance.getAssistanceStatusByDate')
        yield from self.register(self.getAssistanceStatusByUsers_async, 'assistance.getAssistanceStatusByUsers')
        yield from self.register(self.getAssistanceData_async, 'assistance.getAssistanceData')
        yield from self.register(self.getSchedules_async, 'assistance.getSchedules')
        yield from self.register(self.persistSchedule_async, 'assistance.persistSchedule')
        yield from self.register(self.deleteSchedule_async, 'assistance.deleteSchedule')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

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

    def getAssistanceStatusByDate(self, userId, date):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getAssistanceStatusByDate_async(self, sid, userId, date):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getAssistanceStatusByDate, userId, date)
        return r

    def getAssistanceStatusByUsers(self, userIds, dates, status):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getAssistanceStatusByUsers_async(self, sid, userIds, dates, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getAssistanceStatusByUsers, userIds, dates, status)
        return r

    def getAssistanceData(self, userId):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getAssistanceData_async(self, sid, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getAssistanceData, userId)
        return r

    def getSchedules(self, userId, date):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getSchedules_async(self, sid, userId, date):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getSchedules, userId, date)
        return r

    def persistSchedule(self, schedule):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def persistSchedule_async(self, sid, schedule):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistSchedule, schedule)
        return r

    def deleteSchedule(self, id):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def deleteSchedule_async(self, sid, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.deleteSchedule, id)
        return r
