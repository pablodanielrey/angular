# -*- coding: utf-8 -*-
import inject
import logging
import uuid
# import asyncio
# from asyncio import coroutine
# from autobahn.asyncio.wamp import ApplicationSession

from model.offices.entities.office import Office
from model.users.entities.user import User
from model.offices.officeAdminModel import OfficeAdminModel



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

    @autobahn.wamp.register('offices.admin.admin')
    def admin(self, id):
        #administracion de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return OfficeAdminModel.admin(ctx, id)

        finally:
            ctx.closeConn()


    @autobahn.wamp.register('offices.admin.search_users')
    def searchUsers(self, search):
        #busqueda de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return OfficeAdminModel.searchUsers(ctx, search)

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('offices.admin.get_designations')
    def getDesignations(self, placeId):
        #busqueda de designaciones
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return OfficeAdminModel.getDesignations(ctx, placeId)



        finally:
            ctx.closeConn()
