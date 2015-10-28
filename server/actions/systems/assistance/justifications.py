# -*- coding: utf-8 -*-
import logging
import inject
import psycopg2

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
        yield from self.register(self.getJustificationsStock_async, 'assistance.justifications.getJustificationsStock')


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




     def getJustificationsStock(self, sid, userId, justificationId, date, period):
        """
         " Obtener stock de justificacion para una determinada fecha
         " @param userId Identificador de usuario
         """
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
        r = yield from loop.run_in_executor(None, self.getJustificationsStock, sid, userId, justificationId, date, period)
        return r


