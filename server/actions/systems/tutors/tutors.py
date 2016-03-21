# -*- coding: utf-8 -*-
import inject
import logging

from model.tutorias.tutorias import TutoriasModel
from model.login.login import Login
from model.registry import Registry
from model.connection.connection import Connection


"""
    Modulo de acceso a los datos de insercion laboral
"""

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

class TutorsWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        r = inject.instance(Registry)
        self.conn = Connection(r.getRegistry('dcsys'))
        self.tutoriasModel = inject.instance(TutoriasModel)
        self.login = inject.instance(Login)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.search_async, 'tutors.search')
        yield from self.register(self.loadTutorings_async, 'tutors.loadTutorings')
        yield from self.register(self.persist_async, 'tutors.persist')


    def search(self, regex):
        con = self.conn.get()
        try:
            users = self.tutoriasModel.search(con, regex)
            return users

        finally:
            self.conn.put(con)


    def loadTutorings(self, sid):
        con = self.conn.get()
        try:
            userId = self.login.getUserId(sid)
            tutorings = self.tutoriasModel.loadTutorings(con, userId)
            return tutorings
        finally
            self.conn.put(con)

    def persist(self, tutoring):
        con = self.conn.get()
        try:
            id = self.tutoriasModel.persist(con, tutoring)
            con.commit()
            return id
        finally:
            self.conn.put(con)

    @coroutine
    def search_async(self, regex):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.search, regex)
        return r

    @coroutine
    def loadTutorings_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.loadTutorings, sid)
        return r

    @coroutine
    def persist_async(self, tutoring):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persist, tutoring)
        return r
