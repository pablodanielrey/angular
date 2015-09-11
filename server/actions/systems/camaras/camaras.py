# -*- coding: utf-8 -*-
import inject
import logging
import psycopg2

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config
from model.systems.camaras.camaras import Camaras

class WampCamaras(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.camaras = inject.instance(Camaras)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.findAllCamaras_async, 'camaras.camaras.findAllCamaras')
        yield from self.register(self.findRecordings_async, 'camaras.camaras.findRecordings')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)


    def findAllCamaras(self):
        con = self._getDatabase()
        try:
            return self.camaras.findAllCamaras(con)

        finally:
            con.close()

    @coroutine
    def findAllCamaras_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findAllCamaras)
        return r

    def findRecordings(self, start,end,camaras):
        con = self._getDatabase()
        try:
            return self.camaras.findRecordings(con,start,end,camaras)

        finally:
            con.close()

    @coroutine
    def findRecordings_async(self, start,end,camaras):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findRecordings, start,end,camaras)
        return r
