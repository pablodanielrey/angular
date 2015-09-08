# -*- coding: utf-8 -*-
import inject
import logging
import psycopg2

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config
from model.systems.files.files import Files


class FilesWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.files = inject.instance(Files)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.find_async, 'system.files.find')
        yield from self.register(self.upload_async, 'system.files.upload')
        yield from self.register(self.findAllIds, 'system.files.findAllIds')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def findAllIds(self):
        con = self._getDatabase()
        try:
            r = self.files.findAllIds(con)
            return r

        finally:
            con.close()

    def find(self, id):
        con = self._getDatabase()
        try:
            r = self.files.findById(con, id)
            return r

        finally:
            con.close()

    def upload(self, id, name, data):
        con = self._getDatabase()
        try:
            id = self.files.persist(con, id, name, data)
            con.commit()
            return id

        finally:
            con.close()

    @coroutine
    def upload_async(self, id, name, data):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.upload, id, name, data)
        return r

    @coroutine
    def find_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.find, id)
        return r
