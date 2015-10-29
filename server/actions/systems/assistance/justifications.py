# -*- coding: utf-8 -*-
import logging
import inject
import psycopg2
import datetime

from model.exceptions import *
from model.config import Config
from model.systems.assistance.justifications.justifications import Justifications

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession




class JustificationsWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)

        self.justifications = inject.instance(Justifications)




    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getJustifications_async, 'assistance.justifications.getJustifications')
        yield from self.register(self.getJustificationsByUser_async, 'assistance.justifications.getJustificationsByUser')
        yield from self.register(self.getJustificationsStockByUser_async, 'assistance.justifications.getJustificationsStockByUser')
        yield from self.register(self.getJustificationRequestsByDate_async, 'assistance.justifications.getJustificationRequestsByDate')






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



          

    def getJustificationsByUser(self, userId):        
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
    def getJustificationsByUser_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustificationsByUser, userId)
        return r







    def getJustificationsStockByUser(self, sid, userId, justificationId, date, period):   
        """
         " Obtener stock de justificacion para una determinada fecha
         " @param userId Identificador de usuario
         """
        dateAux = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
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




