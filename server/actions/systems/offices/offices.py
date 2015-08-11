# -*- coding: utf-8 -*-
import inject
import logging
import psycopg2

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config
from model.systems.offices.offices import Offices

class OfficesWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.offices = inject.instance(Offices)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getOffices_async, 'offices.offices.getOffices')
        yield from self.register(self.getOfficesByUser_async, 'offices.offices.getOfficesByUser')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def getOfficesByUser(self, userId, tree):
        con = self._getDatabase()
        try:
            return self.offices.getOfficesByUser(con,userId,tree)
        finally:
            con.close()

    @coroutine
    def getOfficesByUser_async(self, userId, tree):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOfficesByUser, userId, tree)
        return r

    def getOffices(self):
        con = self._getDatabase()
        try:
            return self.offices.getOffices(con)

        finally:
            con.close()

    @coroutine
    def getOffices_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOffices)
        return r
