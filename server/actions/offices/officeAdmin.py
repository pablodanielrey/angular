# -*- coding: utf-8 -*-
import inject
import logging
import uuid
# import asyncio
# from asyncio import coroutine
# from autobahn.asyncio.wamp import ApplicationSession

from model.offices.entities.office import Office
from model.offices.entities.officeDesignation import OfficeDesignation
from model.users.entities.user import User
from model.offices.officeModel import OfficeModel



# from model.exceptions import *

import autobahn
import wamp

class OfficeAdmin(wamp.SystemComponentSession):

    @autobahn.wamp.register('offices.admin.get_offices')
    def getOffices(self):
        #busqueda de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return Office.find(ctx).fetch(ctx)

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('offices.admin.get_offices_by_user')
    def getOfficesByUser(self, userId):
        #busqueda de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            if not userId:
                return []

            ods = OfficeDesignation.find(ctx, userId=userId, end=False).fetch(ctx)
            placeIds = [od.placeId for od in ods]

            return Office.find(ctx, id=placeIds).fetch(ctx)

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('offices.admin.admin')
    def admin(self, id):
        #administracion de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            office = None
            if id is not None:
                office = Office.findById(ctx, id)

            if office is None:
                office = Office()

            return office
        finally:
            ctx.closeConn()

    @autobahn.wamp.register('offices.admin.persist')
    def persist(self, office):
        #persistir oficina
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            office.persist(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()



    @autobahn.wamp.register('offices.admin.search_users')
    def searchUsers(self, search):
        #busqueda de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            users = User.search(ctx, search).fetch(ctx)

            for u in users:
                u.label = u.name + " " + u.lastname + " " + u.dni

            return users

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('offices.admin.get_users')
    def getUsers(self, placeId):
        #busqueda de designaciones
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return OfficeModel.getUsers(ctx, placeId)

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('offices.admin.add_user')
    def addUser(self, placeId, userId):
        #busqueda de designaciones
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            od = OfficeDesignation()
            od.userId = userId
            od.placeId = placeId
            od.persist(ctx)
            ctx.con.commit()


        finally:
            ctx.closeConn()


    @autobahn.wamp.register('offices.admin.delete_user')
    def deleteUser(self, placeId, userId):
        #busqueda de designaciones
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            ods = OfficeDesignation.find(ctx, userId=userId, placeId=placeId, end=False).fetch(ctx)

            for od in ods:
                od.delete(ctx)
            ctx.con.commit()


        finally:
            ctx.closeConn()
