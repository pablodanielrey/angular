import inject
import json
import psycopg2
import logging

from model.systems.students.students import Students
from model.events import Events
from model.profiles import Profiles
from model.config import Config


import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession


"""
    Modulo de acceso a los datos de los estudiantes
"""


class StudentsWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.students = inject.instance(Students)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.persist_async, 'system.students.persist')
        yield from self.register(self.findById_async, 'system.students.findById')
        yield from self.register(self.findByNumber_async, 'system.students.findByNumber')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def persist(self, student):
        con = self._getDatabase()
        try:
            self.students.persist(con, student)
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def persist_async(self, student):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persist, student)
        return r

    def findById(self, userId):
        con = self._getDatabase()
        try:
            student = self.students.findById(con, userId)
            return student

        finally:
            con.close()

    @coroutine
    def findById_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findById, userId)
        return r

    def findByNumber(self, n):
        con = self._getDatabase()
        try:
            student = self.students.findByNumber(con, n)
            return student

        finally:
            con.close()

    @coroutine
    def findByNumber_async(self, n):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findByNumber, n)
        return r
