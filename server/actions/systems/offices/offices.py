# -*- coding: utf-8 -*-
import datetime
import logging
logging.getLogger().setLevel(logging.INFO)

import wamp
import autobahn
from twisted.internet.defer import inlineCallbacks

from model.offices.office import Office
from model.offices.officeModel import OfficeModel



import cProfile

def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return profiled_func



class Offices(wamp.SystemComponentSession):

    conn = wamp.getConnectionManager()

    def _getCtx(self, daoType):
        return Context(self.conn.get())

    def _commit(self, ctx):
        ctx.con.commit()

    def _putCtx(self, ctx):
        self.conn.put(ctx.con)


    @autobahn.wamp.register('offices.find_offices_by_user')
    def findOfficesByUser(self, userId, types, tree):
        ctx = self._getCtx(SqlDAO)
        try:
            return Office.findByUser(ctx, userId, types, tree=tree)
        finally:
            self._putCtx(ctx)

    @autobahn.wamp.register('offices.persist')
    @inlineCallbacks
    def persist(self, office):
        ctx = self._getCtx(SqlDAO)
        try:
            id = office.persist(ctx)
            self._commit(ctx)
            yield self.publish('offices.persist_event', id)
            return id
        finally:
            self._putCtx(ctx)






    @autobahn.wamp.register('offices.find_users_by_regex')
    def findUsersByRegex(self, regex):
        logging.info('searchUsers')
        logging.info(regex)
        con = self.conn.get()
        try:
            return OfficeModel.searchUsers(con, regex)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('offices.find_by_id')
    def findById(self, ids):
        con = self.conn.get()
        try:
            offices = Office.findByIds(con, ids)
            for office in offices:
                office.users = OfficeModel.getUsers(con, office.id)
            return offices
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('offices.find_users_by_ids')
    def searchUsers(self, ids):
        con = self.conn.get()
        try:
            return OfficeModel.findUsersByIds(con, ids)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('offices.get_office_types')
    def getOfficeTypes(self):
        return Office.getTypes()


    @autobahn.wamp.register('offices.find_all')
    def findAll(self, types):
        con = self.conn.get()
        try:
            return Office.findAll(con, types)
        finally:
            self.conn.put(con)



    @autobahn.wamp.register('offices.persist_with_users')
    @inlineCallbacks
    def persistWithUsers(self, office, userIds):
        assert office is not None
        assert isinstance(userIds, list)
        con = self.conn.get()
        try:
            id = office.persist(con)
            OfficeModel.persistDesignations(con, id, userIds)
            con.commit()
            yield self.publish('offices.persist_event', id)
            return id
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('offices.remove')
    @inlineCallbacks
    def remove(self, office):
        con = self.conn.get()
        try:
            id = office.remove(con)
            con.commit()
            yield self.publish('offices.remove_event', id)
            return id
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
