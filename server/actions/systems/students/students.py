import inject
import json
import logging

from model.users.users import Student, StudentDAO
from model.registry import registry
from mocel.connection.connection import Connection

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

        r = inject.instance(Registry)
        self.conn = Connection(r.getRegistry('dcsys'))
        self.students = inject.instance(StudentDAO)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.persist_async, 'system.students.persist')
        yield from self.register(self.findById_async, 'system.students.findById')
        #yield from self.register(self.findByNumber_async, 'system.students.findByNumber')

    def persist(self, student):
        con = self.conn.get()
        try:
            sid = self.students.persist(con, student)
            con.commit()
            return sid

        finally:
            self.conn.put(con)

    @coroutine
    def persist_async(self, student):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persist, student)
        return r

    def findById(self, userId):
        con = self.conn.get()
        try:
            students = self.students.findById(con, [userId])
            if len(students) <= 0:
                return None
            return student[0]

        finally:
            self.conn.put(con)

    @coroutine
    def findById_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findById, userId)
        return r

    """
    def findByNumber(self, n):
        con = self.conn.get()
        try:
            student = self.students.findByNumber(con, n)
            return student

        finally:
            self.conn.put(con)

    @coroutine
    def findByNumber_async(self, n):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findByNumber, n)
        return r
    """
