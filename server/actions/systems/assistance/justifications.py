# -*- coding: utf-8 -*-
import logging
import inject
import datetime

from model.login.login import Login
from model.login.session import SessionDAO, Session

import model.assistance.date
from model.assistance.justifications import Justifications
from model.registry import Registry

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.connection import connection



class JustificationsWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        reg = inject.instance(Registry)

        self.conn = connection.Connection(reg.getRegistry('dcsys'))

        self.login = inject.instance(Login)
        self.date = inject.instance(model.assistance.date.Date)
        self.justifications = inject.instance(Justifications)


    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')

        yield from self.register(self.updateJustificationRequestStatus_async, 'assistance.justifications.updateJustificationRequestStatus')
        yield from self.register(self.getJustificationRequests_async, 'assistance.justifications.getJustificationRequests')
        yield from self.register(self.requestJustification_async, 'assistance.justifications.requestJustification')
        yield from self.register(self.getJustificationRequestsByDate_async, 'assistance.justifications.getJustificationsRequestsByDate')
        yield from self.register(self.requestJustificationRange_async, 'assistance.justifications.requestJustificationRange')
        yield from self.register(self.getJustificationsStockByUser_async, 'assistance.justifications.getJustificationsStockByUser')
        yield from self.register(self.getJustifications_async, 'assistance.justifications.getJustifications')
        yield from self.register(self.getJustificationsByUser_async, 'assistance.justifications.getJustificationsByUser')



    def getJustifications(self, sid):
        """
         " Obtener justificaciones a partir del session id
         " @param sid Identificador de session
         """

        con = self.conn.get()
        try:
            justifications = self.justifications.getJustifications(con)
            return justifications

        finally:
            self.conn.put(con)


    @coroutine
    def getJustifications_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustifications, sid)
        return r


    def getJustificationsByUser(self, sid, userId):
        """
         " Obtener justificaciones del usuario
         " @param userId Identificador de usuario
         """
        con = self.conn.get()
        try:

            justifications = self.justifications.getJustificationsByUser(con, userId)
            return justifications

        finally:
            self.conn.put(con)

    @coroutine
    def getJustificationsByUser_async(self, sid, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationsByUser, sid, userId)
        return r


    def getJustificationsStockByUser(self, sid, userId, justificationId, date, period):
        """
         " Obtener stock de justificacion para una determinada fecha
         " @param userId Identificador de usuario
         """
        if (date is not None):
            dateAux = datetime.datetime.strptime(date[0:19], "%Y-%m-%dT%H:%M:%S")
        else:
            dateAux = datetime.datetime.now()
        con = self.conn.get()
        try:
            justificationsStock = self.justifications.getJustificationStock(con, userId, justificationId, dateAux, period)

            return justificationsStock

        finally:
            self.conn.put(con)

    @coroutine
    def getJustificationsStockByUser_async(self, sid, userId, justificationId, date, period):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationsStockByUser, sid, userId, justificationId, date, period)
        return r




    def getJustificationRequestsByDate(self, userIds=None, start=None, end=None, statusList=[]):
        """
         " Obtener requerimientos de justificaciones para un determinado rango de fechas, para una determinada lista de usuario, para una determinada lista de estados
         " @param userIds Lista con ids de usuario
         " @param start Timestamp de inicio
         " @param end Timestamp de fin
         " @param statusList Lista de estados
         """
        startAux = None if(start is None) else datetime.datetime.strptime(start[0:10], "%Y-%m-%d")
        endAux = None if(end is None) else datetime.datetime.strptime(end[0:10], "%Y-%m-%d")

        con = self.conn.get()
        try:
            justificationsRequest = self.justifications.getJustificationRequestsByDate(con, statusList, userIds, startAux, endAux)
            return justificationsRequest

        finally:
            self.conn.put(con)


    @coroutine
    def getJustificationRequestsByDate_async(self, sid, userIds, start, end, statusList):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationRequestsByDate, userIds, start, end, statusList)
        return r

    def getJustificationRequests(self, sid, status, userIds):
        """
           obtener requerimientos de justificaciones
        """
        con = self.conn.get()
        try:

            justificationRequests = self.justifications.getJustificationRequests(con, status, userIds)
            return justificationRequests

        finally:
            self.conn.put(con)

    @coroutine
    def getJustificationRequests_async(self, sid, status, userIds):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationRequests, sid, status, userIds)
        return r


    def requestJustification(self, sid, status, userId,requestor_id,justificationId,begin,end):
        con = self.conn.get()
        try:
            if begin is not None:
                begin = self.date.parse(begin)
            if end is not None:
                end = self.date.parse(end)
            events = self.justifications.requestJustification(con,userId,requestor_id,justificationId,begin,end,status)
            con.commit()

            for e in events:
                if 'type' in e and 'data' in e:
                    self.publish('assistance.justification.' + e['type'], e['data'])
            return True

        finally:
            self.conn.put(con)

    @coroutine
    def requestJustification_async(self, sid, status, userId,requestor_id,justificationId,begin,end=None):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.requestJustification, sid, status, userId,requestor_id,justificationId,begin,end)
        return r


    def requestJustificationRange(self, userId,requestor_id,justificationId,begin,end, status):
        con = self.conn.get()
        try:
            if begin is None or end is None:
                return None
            begin = self.date.parse(begin)
            end = self.date.parse(end)
            events = self.justifications.requestJustificationRange(con,userId,requestor_id,justificationId,begin,end,status)
            con.commit()
            for e in events:
                if 'type' in e and 'data' in e:
                    self.publish('assistance.justification.' + e['type'], e['data'])
            return True
        finally:
            self.conn.put(con)

    @coroutine
    def requestJustificationRange_async(self, sid, userId,requestor_id,justificationId,begin,end, status='PENDING'):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.requestJustificationRange, userId,requestor_id,justificationId,begin,end, status)
        return r


    def updateJustificationRequestStatus(self, sid, requestId, status):
        con = self.conn.get()
        try:
            userId = self.login.getUserId(sid)
            events = self.justifications.updateJustificationRequestStatus(con,userId,requestId,status)
            con.commit()
            for e in events:
                if 'type' in e and 'data' in e:
                    self.publish('assistance.justification.' + e['type'], e['data'])

            return True

        finally:
            self.conn.put(con)

    @coroutine
    def updateJustificationRequestStatus_async(self, sid, requestId, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.updateJustificationRequestStatus, sid, requestId, status)
        return r
