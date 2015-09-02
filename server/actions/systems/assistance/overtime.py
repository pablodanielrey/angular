# -*- coding: utf-8 -*-
import json
import base64
import datetime
import logging
import inject
import psycopg2
from model.exceptions import *

from model.config import Config
from model.profiles import Profiles
from model.events import Events

from model.systems.assistance.assistance import Assistance
from model.systems.assistance.date import Date
from model.systems.assistance.justifications.justifications import Justifications
from model.systems.assistance.overtime import Overtime

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession


class OvertimeWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getRequests_async, 'assistance.overtime.getRequests')
        yield from self.register(self.getRequestsToManage_async, 'assistance.overtime.getRequestsToManage')
        yield from self.register(self.requestOvertime_async, 'assistance.overtime.requestOvertime')
        yield from self.register(self.persistStatus_async, 'assistance.overtime.persistStatus')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def getRequests(self, status):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getRequests_async(self, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getRequests, status)
        return r

    def getRequestsToManage(self, status, group):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getRequestsToManage_async(self, status, group):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getRequestsToManage, status, group)
        return r

    def requestOvertime(self, userId, request):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def requestOvertime_async(self, userId, request):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.requestOvertime, userId, request)
        return r

    def persistStatus(self, requestId, status):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def persistStatus_async(self, requestId, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistStatus, requestId, status)
        return r
