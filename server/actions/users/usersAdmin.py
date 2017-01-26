# -*- coding: utf-8 -*-
import inject
import logging
import uuid
# import asyncio
# from asyncio import coroutine
# from autobahn.asyncio.wamp import ApplicationSession

from model.users.usersAdminModel import UsersAdminModel
from model.users.entities.user import User
from model.users.entities.mail import Mail


# from model.exceptions import *

import autobahn
import wamp

class UsersAdmin(wamp.SystemComponentSession):

    @autobahn.wamp.register('users.admin.search')
    def search(self, search):
        #busqueda de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return User.search(ctx, search).fetch(ctx)

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.admin.admin')
    def admin(self, id):
        #administracion de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return UsersAdminModel.admin(ctx, id)

        finally:
            ctx.closeConn()


    @autobahn.wamp.register('users.admin.find_emails_by_user_id')
    def findEmailsByUserId(self, userId):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return Mail.find(ctx, userId=userId).fetch(ctx)

        finally:
            ctx.closeConn()


    @autobahn.wamp.register('users.admin.add_email')
    def addEmail(self, email):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            email.persist(ctx)
            ctx.con.commit()
            return email

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.admin.delete_email')
    def deleteEmail(self, email):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            email.delete(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.admin.persist')
    def persist(self, user):
        #administracion de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            UsersAdminModel.persist(ctx, user)
            ctx.con.commit()

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.admin.find_by_ids')
    def findByIds(self, ids):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return User.findByIds(ctx, ids)

        finally:
            ctx.closeConn()
