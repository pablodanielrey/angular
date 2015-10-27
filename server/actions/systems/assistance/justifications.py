# -*- coding: utf-8 -*-
import inject
import re
import psycopg2
import time
import logging

from model.exceptions import *

from model.config import Config
from model.profiles import Profiles
from model.events import Events
from model.users.users import Users
from model.mail.mail import Mail

from model.systems.assistance.assistance import Assistance
from model.systems.assistance.date import Date
from model.systems.assistance.justifications.justifications import Justifications
from model.systems.offices.offices import Offices

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession


class JustificationsWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.date = inject.attr(Date)
        self.events = inject.attr(Events)
        self.mail = inject.attr(Mail)
        self.users = inject.attr(Users)
        self.offices = inject.attr(Offices)
        self.justifications = inject.attr(Justifications)
  
    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getJustifications_async, 'assistance.justifications.getJustifications')
        yield from self.register(self.getJustificationsByUser_async, 'assistance.justifications.getJustificationsByUser')
        yield from self.register(self.getJustificationsStock_async, 'assistance.justifications.getJustificationsStock')
        yield from self.register(self.updateJustificationStock_async, 'assistance.justifications.updateJustificationStock')
        yield from self.register(self.getJustificationsRequestsByDate_async, 'assistance.justifications.getJustificationsRequestsByDate')
        yield from self.register(self.getJustificationsRequestsToManage_async, 'assistance.justifications.getJustificationsRequestsToManage')
        yield from self.register(self.getJustificationsRequests_async, 'assistance.justifications.getJustificationsRequests')
        yield from self.register(self.updateJustificationRequestStatus_async, 'assistance.justifications.updateJustificationRequestStatus')
        yield from self.register(self.requestJustification_async, 'assistance.justifications.requestJustification')
        yield from self.register(self.requestJustificationRange_async, 'assistance.justifications.requestJustificationRange')
        yield from self.register(self.getSpecialJustifications_async, 'assistance.justifications.getSpecialJustifications')
        yield from self.register(self.requestGeneralJustification_async, 'assistance.justifications.requestGeneralJustification')
        yield from self.register(self.requestGeneralJustificationRange_async, 'assistance.justifications.requestGeneralJustificationRange')
        yield from self.register(self.getGeneralJustificationRequests_async, 'assistance.justifications.getGeneralJustificationRequests')
        yield from self.register(self.deleteGeneralJustificationRequest_async, 'assistance.justifications.deleteGeneralJustificationRequest')


    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def getJustifications(self):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getJustifications_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustifications)
        return r



    def getJustificationsByUser(self, userId):
        '''
        Obtener justificaciones del usuario
        @param userId Id del usuario
        '''
        
        con = self._getDatabase()
        try:
            justifications = self.justifications.getJustificationsByUser(con, userId)
            return justifications

        finally:
            con.close()

    @coroutine
    def getJustificationsByUser_async(self, sid, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationsByUser, userId)
        return r




    def getJustificationsStock(self, userId, justificationId, date, period):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getJustificationsStock_async(self, sid, userId, justificationId, date, period):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationsStock, userId, justificationId, date, period)
        return r

    def updateJustificationStock(self, userId, justificationId, stock):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def updateJustificationStock_async(self, sid, userId, justificationId, stock):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.updateJustificationStock, userId, justificationId, stock)
        return r

    def getJustificationsRequestsByDate(self, userIds, start, end, status):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getJustificationsRequestsByDate_async(self, sid, userIds, start, end, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationsRequestsByDate, userIds, start, end, status)
        return r

    def getJustificationsRequestsToManage(self, status, group):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getJustificationsRequestsToManage_async(self, sid, status, group):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationsRequestsToManage, status, group)
        return r

    def getJustificationsRequests(self, status):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getJustificationsRequests_async(self, sid, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationsRequests, status)
        return r

    def updateJustificationRequestStatus(self, requestId, status):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def updateJustificationRequestStatus_async(self, sid, requestId, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.updateJustificationRequestStatus, requestId, status)
        return r

    def requestJustification(self, userId, justification, status):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def requestJustification_async(self, sid, userId, justification, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.requestJustification, userId, justification, status)
        return r

    def requestJustificationRange(self, userId, justificationId, start, end, status):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def requestJustificationRange_async(self, sid, userId, justificationId, start, end, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.requestJustification, userId, justificationId, start, end, status)
        return r

    def getSpecialJustifications(self, sid):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getSpecialJustifications_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getSpecialJustifications, sid)
        return r

    def reguestGeneralJustification(self, sid, justification):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def requestGeneralJustification_async(self, sid, justification):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.requestGeneralJustification, sid, justification)
        return r

    def reguestGeneralJustificationRange(self, sid, justification):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def requestGeneralJustificationRange_async(self, sid, justification):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.requestGeneralJustificationRange, sid, justification)
        return r

    def getGeneralJustificationRequests(self, sid):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getGeneralJustificationRequests_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getGeneralJustificationRequests, sid)
        return r

    def deleteGeneralJustificationRequest(self, sid, requestId):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def deleteGeneralJustificationRequest_async(self, sid, requestId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.deleteGeneralJustificationRequest, sid, requestId)
        return r
