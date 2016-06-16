# -*- coding: utf-8 -*-
import logging
import inject

from model.login.profiles import ProfileDAO
from model.offices.offices import Office


from model.registry import Registry
from model.connection import connection
from model.login.login import Login

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.serializer.utils import  JSONSerializable

class OfficeWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        reg = inject.instance(Registry)

        self.conn = connection.Connection(reg.getRegistry('dcsys'))
        self.loginModel = inject.instance(Login)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getOfficesByUserRole_async, 'office.getOfficesByUserRole')
        yield from self.register(self.findById_async, 'office.findById')
        yield from self.register(self.getOfficesUsers_async, 'office.getOfficesUsers')

    def getOfficesByUserRole(self, userId, tree, role):
        con = self.conn.get()
        try:
            return Office.getOfficesByUserRole(con, userId, tree, role)
        finally:
            self.conn.put(con)

    @coroutine
    def getOfficesByUserRole_async(self, userId, tree = False, role = 'autoriza'):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOfficesByUserRole, userId, tree, role)
        return r

    def findById(self, ids):
        con = self.conn.get()
        try:
            return Office.findById(con, ids)
        finally:
            self.conn.put(con)

    @coroutine
    def findById_async(self, ids):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findById, ids)
        return r

    def getOfficesUsers(self, ids):
        con = self.conn.get()
        try:
            return Office.getOfficesUsers(con, ids)
        finally:
            self.conn.put(con)

    @coroutine
    def getOfficesUsers_async(self, ids):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOfficesUsers, ids)
        return r
