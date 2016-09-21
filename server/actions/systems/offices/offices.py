# -*- coding: utf-8 -*-
import autobahn

from model.offices.offices import Office
import wamp

class Offices(wamp.SystemComponentSession):

    conn = wamp.getConnectionManager()

    @autobahn.wamp.register('offices.find_offices_by_user')
    def findOfficesByUser(self, userId, tree):
        con = self.conn.get()
        try:
            return Office.getOfficesByUser(con, userId, tree)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('offices.find_by_id')
    def findById(self, ids):
        con = self.conn.get()
        try:
            return Office.findById(con, ids)
        finally:
            self.conn.put(con)


"""

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
        yield from self.register(self.getOfficesByUser_async, 'office.getOfficesByUser')
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

    def getOfficesByUser(self, userId, tree):

    @coroutine
    def getOfficesByUser_async(self, userId, tree = False):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOfficesByUser, userId, tree)
        return r

    def findById(self, ids):

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
"""
