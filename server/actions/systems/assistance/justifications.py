# -*- coding: utf-8 -*-
import logging
import inject
import psycopg2
import datetime

from model.exceptions import *
from model.config import Config
from model.systems.assistance.justifications.justifications import Justifications
import model.systems.assistance.date

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession




class JustificationsWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.date = inject.instance(model.systems.assistance.date.Date)

        self.justifications = inject.instance(Justifications)




    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getJustifications_async, 'assistance.justifications.getJustifications')
        yield from self.register(self.getJustificationsByUser_async, 'assistance.justifications.getJustificationsByUser')
        yield from self.register(self.getJustificationsStockByUser_async, 'assistance.justifications.getJustificationsStockByUser')
        yield from self.register(self.getJustificationRequestsByDate_async, 'assistance.justifications.getJustificationRequestsByDate')
        yield from self.register(self.getJustificationRequestsToManage_async, 'assistance.justifications.getJustificationRequestsToManage')
        yield from self.register(self.updateJustificationStock_async, 'assistance.justifications.updateJustificationStock')
        yield from self.register(self.getGeneralJustificationRequests_async, 'assistance.justifications.getGeneralJustificationRequests')
        yield from self.register(self.deleteGeneralJustificationRequest_async, 'assistance.justifications.deleteGeneralJustificationRequest')
        yield from self.register(self.requestGeneralJustification_async, 'assistance.justifications.requestGeneralJustification')
        yield from self.register(self.requestGeneralJustificationRange_async, 'assistance.justifications.requestGeneralJustificationRange')
        yield from self.register(self.getJustificationRequests_async, 'assistance.justifications.getJustificationRequests')







    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)





    def getJustifications(self, sid):
        """
         " Obtener justificaciones a partir del session id
         " @param sid Identificador de session
         """

        con = self._getDatabase()
        try:
            justifications = self.justifications.getJustifications(con)
            return justifications

        finally:
            con.close()


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
        con = self._getDatabase()
        try:

            justifications = self.justifications.getJustificationsByUser(con, userId)
            return justifications

        finally:
            con.close()

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
        con = self._getDatabase()
        try:
            justificationsStock = self.justifications.getJustificationStock(con, userId, justificationId, dateAux, period)

            return justificationsStock

        finally:
            con.close()

    @coroutine
    def getJustificationsStockByUser_async(self, sid, userId, justificationId, date, period):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationsStockByUser, sid, userId, justificationId, date, period)
        return r




    def getJustificationRequestsByDate(self, userIds=None, start=None, end=None, statusList=None):
        """
         " Obtener requerimientos de justificaciones para un determinado rango de fechas, para una determinada lista de usuario, para una determinada lista de estados
         " @param userIds Lista con ids de usuario
         " @param start Timestamp de inicio
         " @param end Timestamp de fin
         " @param statusList Lista de estados
         """

        startAux = None if(start is None) else datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        endAux = None if(start is None) else datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

        con = self._getDatabase()
        try:
            justificationsRequest = self.justifications.getJustificationRequestsByDate(con, statusList, userIds, startAux, endAux)
            return justificationsRequest

        finally:
            con.close()

    @coroutine
    def getJustificationRequestsByDate_async(self, sid, userIds, start, end, statusList):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationRequestsByDate, userIds, start, end, statusList)
        return r




    def getJustificationRequestsToManage(self, userId, statusList, group):
        """
         " Obtener requerimientos de justificaciones para ser administradas
         " @param userId Id de usuario administrador de justificaciones
         " @param statusList Lista de estados
         " @param group grupo a partir del cual se obtendran las justificaciones
         """
        con = self._getDatabase()
        try:
            justificationsRequest = self.justifications.getJustificationRequestsToManage(con,userId,statusList,group)
            return justificationsRequest

        finally:
            con.close()

    @coroutine
    def getJustificationRequestsToManage_async(self, sid, userId, statusList, group):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationRequestsToManage, userId, statusList, group)
        return r




    def updateJustificationStock(self, userId, justificationId, stock):

        """
         " actualizar stock para un determinado usuario
         " @param userId usuario al cual se le actualizara la justifiacion
         " @param justificationId Id de la justificacion a actualizar
         " @param stock Nuevo stock, dependiendo de la justificacion variara el tipo y el valor, generalmente es un entero correspondiente a los dias o segundos
        """
        con = self._getDatabase()
        try:
            event = self.justifications.updateJustificationStock(con, userId, justificationId, stock)
            con.commit()
            return event;

        finally:
            con.close()

    @coroutine
    def updateJustificationStock_async(self, sid, userId, justificationId, stock):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.updateJustificationStock, userId, justificationId, stock)
        return r



    def getGeneralJustificationRequests(self, sid):
        """
           Obtener justificaciones generales
        """
        con = self._getDatabase()
        try:
            return self.justifications.getGeneralJustificationRequests(con)

        finally:
            con.close()

    @coroutine
    def getGeneralJustificationRequests_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getGeneralJustificationRequests, sid)
        return r



    def deleteGeneralJustificationRequest(self, requestId):
        """
           Eliminar solicitud de justificacion general
        """
        con = self._getDatabase()
        try:
            justification = self.justifications.deleteGeneralJustificationRequest(con, requestId)

            con.commit()
            return justification;


        finally:
            con.close()




    @coroutine
    def deleteGeneralJustificationRequest_async(self, sid, requestId):
        """
           Eliminar justificacion general
        """
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.deleteGeneralJustificationRequest, requestId)
        return r






    def requestGeneralJustification(self, sid, justificationId, begin):
        """
           Solicitar justificacion general en una determinada fecha
        """
        con = self._getDatabase()
        try:
            self.justifications.requestGeneralJustification(con, justificationId, begin)
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def requestGeneralJustification_async(self, sid, justificationId, begin):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.requestGeneralJustification, sid, justificationId, begin)
        return r




    def requestGeneralJustificationRange(self, sid, justificationId, begin, end):
        """
           Solicitar justificacion general en un rango
        """
        con = self._getDatabase()
        try:
            if begin is None or end is None:
                return None
            begin = self.date.parse(begin)
            end = self.date.parse(end)
            self.justifications.requestGeneralJustificationRange(con, justificationId, begin, end)
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def requestGeneralJustificationRange_async(self, sid, justificationId, begin, end):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.requestGeneralJustificationRange, sid, justificationId, begin, end)
        return r




    def getJustificationRequests(self, sid, status, userIds):
        print("**************** getJustificationRequests")
        print(status)
        print(userIds)
        """
           obtener requerimientos de justificaciones
        """
        con = self._getDatabase()
        try:
            justificationRequests = self.justifications.getJustificationRequests(con, None, userIds)
            return justificationRequests

        finally:
            con.close()

    @coroutine
    def getJustificationRequests_async(self, sid, status, userIds):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationRequests, sid, status, userIds)
        return r
