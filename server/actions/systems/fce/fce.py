# -*- coding: utf-8 -*-
import inject
import json
import uuid
import re
import logging
import psycopg2
import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.registry import Registry
from model.connection.connection import Connection

from model.users.users import User, UserPassword
from model.login.login import Login
from model.systems.systems import Systems

class FceWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        registry = inject.instance(Registry)
        self.reg = registry.getRegistry('dcsys')
        self.conn = Connection(self.reg)
        self.loginModel = inject.instance(Login)
        self.systemsModel = inject.instance(Systems)

    @coroutine
    def onJoin(self, details):
        yield from self.register(self.listSystems_async, 'fce.listSystems')
        yield from self.register(self.changePassword_async, 'fce.changePassword')


    def listSystems(self, sid):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            systems = Systems.listSystems(con, userId)
            return systems

        finally:
            self.conn.put(con)

    @coroutine
    def listSystems_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.listSystems, sid)
        return r


    def changePassword(self, sid, password):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)

            passwords = UserPassword.findByUserId(con, userId)
            for passwd in passwords:
                passwd.setPassword(password)
                passwd.persist(con)

            con.commit()
        finally:
            self.conn.put(con)

    @coroutine
    def changePassword_async(self, sid, password):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.changePassword, sid, password)
        return r
