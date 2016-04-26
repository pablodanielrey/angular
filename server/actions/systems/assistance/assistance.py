# -*- coding: utf-8 -*-
import logging
import inject
import dateutil.parser
from datetime import datetime, date, time, timedelta

from model.login.profiles import ProfileDAO
from model.assistance.assistance import AssistanceModel, AssistanceData

import dateutil, dateutil.tz, dateutil.parser, datetime

from model.registry import Registry
from model.connection import connection

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.serializer.utils import  JSONSerializable

class AssistanceWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        reg = inject.instance(Registry)

        self.conn = connection.Connection(reg.getRegistry('dcsys'))
        # self.profiles = inject.instance(ProfileDAO)

        self.assistance = inject.instance(AssistanceModel)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getAssistanceData_async, 'assistance.getAssistanceData')

    def _localizeLocal(self,naive):
        tz = dateutil.tz.tzlocal()
        local = naive.replace(tzinfo=tz)
        return local

    def _isNaive(self, date):
        return not ((date.tzinfo != None) and (date.tzinfo.utcoffset(date) != None))

    def _parseDate(self, datestr):
        dt = dateutil.parser.parse(datestr)
        if self._isNaive(dt):
            dt = self._localizeLocal(dt)
        return dt

    def getAssistanceData(self, userIds, startStr, endStr):
        con = self.conn.get()
        try:
            start = self._parseDate(startStr)
            end = self._parseDate(endStr)
            return self.assistance.getAssistanceData(con, userIds, start, end)
        finally:
            self.conn.put(con)

    @coroutine
    def getAssistanceData_async(self, userIds, start, end):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getAssistanceData, userIds, start, end)
        return r
