# -*- coding: utf-8 -*-
import inject
import logging

from model.tutorias.tutorias import TutoriasModel, Tutoring, TutoringSituation, TutoringDAO

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

    def _createSchemas(self):
        con = self.conn.get()
        try:
            TutoringDAO._createSchemas(con)
            con.commit()

        finally:
            self.conn.put(con)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.search_async, 'tutors.search')
        yield from self.register(self.findByTutorId_async, 'tutors.findByTutorId')
        yield from self.register(self.persist_async, 'tutors.persist')
        yield from self.register(self.delete_async, 'tutors.delete')


    def delete(self, tid):
        con = self.conn.get()
        try:
            ok = self.tutoriasModel.delete(con, tid)
            con.commit()
            return ok

        finally:
            self.conn.put(con)


    def search(self, regex):
        con = self.conn.get()
        try:
            users = self.tutoriasModel.search(con, regex)
            return users

        finally:
            self.conn.put(con)

    def _serializeUser(self, u):
        u.telephones = [ t.__dict__ for t in u.telephones ]
        return u.__dict__

    def _serializeSituation(self, s):
        s.user['user'] = self._serializeUser(s.user['user'])
        s.user['student'] = s.user['student'].__dict__
        return s.__dict__

    def findByTutorId(self, tId):
        con = self.conn.get()
        try:
            tutorings = self.tutoriasModel.findByTutorId(con, tId)
            for t in tutorings:
                t.tutor = self._serializeUser(t.tutor)
                t.situations = [ self._serializeSituation(s) for s in t.situations ]
            tutorings = [ t.__dict__ for t in tutorings ]

            return tutorings

        finally:
            self.conn.put(con)

    def persist(self, tut):
        con = self.conn.get()
        try:
            tutoring = Tutoring()
            tutoring.__dict__ = tut
            situations = []
            for t2 in tut['situations']:
                t = TutoringSituation()
                t.__dict__ = t2
                situations.append(t)
            tutoring.situations = situations
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
    def findByTutorId_async(self, tid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findByTutorId, tid)
        return r

    @coroutine
    def persist_async(self, tutoring):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persist, tutoring)
        return r

    @coroutine
    def delete_async(self, tid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.delete, tid)
        return r
