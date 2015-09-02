# -*- coding: utf-8 -*-
import inject
import logging
import psycopg2

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config
from model.profiles import Profiles
from model.systems.assystance.positions import Positions


class PositionsWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.profiles = inject.attr(Profiles)
        self.positions = inject.attr(Positions)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getPosition_async, 'positions.getPosition')
        yield from self.register(self.updatePosition_async, 'positions.updatePosition')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def getPosition(self, sid, userId):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getPosition_async(self, sid, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getPosition, sid, userId)
        return r

    def updatePosition(self, sid, userId, position):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def updatePosition_async(self, sid, userId, position):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.updatePosition, sid, userId, position)
        return r
