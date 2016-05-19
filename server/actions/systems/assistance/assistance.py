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
from model.login.login import Login

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
        self.loginModel = inject.instance(Login)

        self.assistance = inject.instance(AssistanceModel)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getAssistanceData_async, 'assistance.getAssistanceData')
        yield from self.register(self.getJustifications_async, 'assistance.getJustifications')
        yield from self.register(self.createSingleDateJustification_async, 'assistance.createSingleDateJustification')
        yield from self.register(self.createRangedTimeWithReturnJustification_async, 'assistance.createRangedTimeWithReturnJustification')
        yield from self.register(self.createRangedTimeWithoutReturnJustification_async, 'assistance.createRangedTimeWithoutReturnJustification')
        yield from self.register(self.createRangedJustification_async, 'assistance.createRangedJustification')
        yield from self.register(self.changeStatus_async, 'assistance.changeStatus')
        yield from self.register(self.getJustificationData_async, 'assistance.getJustificationData')

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

    def getJustifications(self, userId, startStr, endStr, isAll):
        con = self.conn.get()
        try:
            start = self._parseDate(startStr)
            end = self._parseDate(endStr)
            return self.assistance.getJustifications(con, userId, start, end, isAll)
        finally:
            self.conn.put(con)

    @coroutine
    def getJustifications_async(self, userId, start, end, isAll):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustifications, userId, start, end, isAll)
        return r

    def createSingleDateJustification(self, sid, dateStr, userId, justClazz, justModule, ownerId = None):
        con = self.conn.get()
        try:
            if ownerId is None:
                ownerId = self.loginModel.getUserId(con, sid)
            date = self._parseDate(dateStr)
            self.assistance.createSingleDateJustification(con, date, userId, ownerId, justClazz, justModule)
            con.commit()
        finally:
            self.conn.put(con)

    @coroutine
    def createSingleDateJustification_async(self, sid, date, userId, justClazz, justModule, ownerId = None):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.createSingleDateJustification, sid, date, userId, justClazz, justModule, ownerId)
        return r

    def createRangedTimeWithReturnJustification(self, sid, startStr, endStr, userId, justClazz, justModule, ownerId = None):
        con = self.conn.get()
        try:
            if ownerId is None:
                ownerId = self.loginModel.getUserId(con, sid)
            start = self._parseDate(startStr)
            end = self._parseDate(endStr)
            self.assistance.createRangedTimeWithReturnJustification(con, start, end, userId, ownerId, justClazz, justModule)
            con.commit()
        finally:
            self.conn.put(con)

    @coroutine
    def createRangedTimeWithReturnJustification_async(self, sid, start, end, userId, justClazz, justModule, ownerId = None):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.createRangedTimeWithReturnJustification, sid, start, end, userId, justClazz, justModule, ownerId)
        return r

    def createRangedTimeWithoutReturnJustification(self, sid, startStr, userId, justClazz, justModule, ownerId = None):
        con = self.conn.get()
        try:
            if ownerId is None:
                ownerId = self.loginModel.getUserId(con, sid)
            start = self._parseDate(startStr)
            self.assistance.createRangedTimeWithoutReturnJustification(con, start, userId, ownerId, justClazz, justModule)
            con.commit()
        finally:
            self.conn.put(con)

    @coroutine
    def createRangedTimeWithoutReturnJustification_async(self, sid, start, userId, justClazz, justModule, ownerId = None):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.createRangedTimeWithoutReturnJustification, sid, start, userId, justClazz, justModule, ownerId)
        return r


    def createRangedJustification(self, sid, startStr, days, userId, justClazz, justModule, ownerId = None):
        con = self.conn.get()
        try:
            if ownerId is None:
                ownerId = self.loginModel.getUserId(con, sid)
            start = self._parseDate(startStr)
            days = int(days)
            self.assistance.createRangedJustification(con, start, days, userId, ownerId, justClazz, justModule)
            con.commit()
        finally:
            self.conn.put(con)

    @coroutine
    def createRangedJustification_async(self, sid, start, days, userId, justClazz, justModule, ownerId = None):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.createRangedJustification, sid, start, days, userId, justClazz, justModule, ownerId)
        return r

    def changeStatus(self, sid, just, status):
        '''
            status = UNDEFINED, PENDING, APPROVED, REJECTED, CANCELED
        '''
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            self.assistance.changeStatus(con, just, status, userId)
            con.commit()
        finally:
            self.conn.put(con)

    @coroutine
    def changeStatus_async(self, sid, just, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.changeStatus, sid, just, status)
        return r

    def getJustificationData(self, userId, dateStr, justClazz, justModule):
        con = self.conn.get()
        try:
            date = self._parseDate(dateStr)
            return self.assistance.getJustificationData(con, userId, date, justClazz, justModule)
        finally:
            self.conn.put(con)

    @coroutine
    def getJustificationData_async(self, userId, date, justClazz, justModule):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationData, userId, date, justClazz, justModule)
        return r
