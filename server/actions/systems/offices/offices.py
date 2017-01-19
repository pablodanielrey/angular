# -*- coding: utf-8 -*-
import datetime
import logging
logging.getLogger().setLevel(logging.INFO)

import wamp
import autobahn
from twisted.internet.defer import inlineCallbacks

from model.offices.entities.office import Office
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

    @autobahn.wamp.register('offices.find_offices_by_user')
    def findOfficesByUser(self, userId, types, tree):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return Office.findByUser(ctx, userId, types, tree=tree)
        finally:
            ctx.closeConn()

    @autobahn.wamp.register('offices.persist')
    @inlineCallbacks
    def persist(self, office):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            id = office.persist(ctx)
            ctx.con.commit()
            yield self.publish('offices.persist_event', id)
            return id
        finally:
            ctx.closeConn()


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
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return Office.find(ctx, type=types)
        finally:
            ctx.closeConn()




    @autobahn.wamp.register('offices.persist_with_users')
    @inlineCallbacks
    def persistWithUsers(self, office, userIds):
        assert office is not None
        assert isinstance(userIds, list)
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            office.persist(con)
            OfficeModel.persistDesignations(ctx, office.id, userIds)
            ctx.con.commit()
            yield self.publish('offices.persist_event', office.id)
            return office.id
        finally:
            ctx.closeConn()


    @autobahn.wamp.register('offices.remove')
    @inlineCallbacks
    def remove(self, office):
        ctx = wamp.getContextManager()
        ctx.getConn()

        try:
            office.delete(ctx)
            ctx.con.commit()
            yield self.publish('offices.remove_event', office.id)
            return office.id
        finally:
            ctx.closeConn()
