# -*- coding: utf-8 -*-
import inject
import logging
import uuid
# import asyncio
# from asyncio import coroutine
# from autobahn.asyncio.wamp import ApplicationSession

#from model.users.usersProfileModel import UsersProfileModel
from model.users.entities.user import User
from model.users.entities.mail import Mail




# from model.exceptions import *

import autobahn
import wamp

class UsersProfile(wamp.SystemComponentSession):

    @autobahn.wamp.register('users.profile.find_by_id')
    def findById(self, id):
        #administracion de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return User.findById(ctx, id)

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.profile.find_emails_by_user_id')
    def findEmailsByUserId(self, userId):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return Mail.find(ctx, userId=userId).fetch(ctx)

        finally:
            ctx.closeConn()


    @autobahn.wamp.register('users.profile.add_email')
    def addEmail(self, email):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            email.persist(ctx)
            ctx.con.commit()
            return email

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.profile.delete_email')
    def deleteEmail(self, email):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            email.delete(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.profile.persist')
    def persist(self, user):
        #administracion de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            user.persist(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()
