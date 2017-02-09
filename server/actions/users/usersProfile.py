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
from model.users.usersModel import UsersModel




# from model.exceptions import *

import autobahn
import wamp

class UsersProfile(wamp.SystemComponentSession):

    def getRegisterOptions(self):
        return autobahn.wamp.RegisterOptions(details_arg='details')

    @autobahn.wamp.register('users.profile.find_by_id')
    def findById(self, id, details):
        #administracion de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return User.findById(ctx, id)

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.profile.find_emails_by_user_id')
    def findEmailsByUserId(self, userId, details):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return Mail.find(ctx, userId=userId).fetch(ctx)

        finally:
            ctx.closeConn()


    @autobahn.wamp.register('users.profile.add_email')
    def addEmail(self, email, details):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            email.persist(ctx)
            ctx.con.commit()
            return email

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.profile.delete_email')
    def deleteEmail(self, email, details):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            email.delete(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.profile.persist')
    def persist(self, user, details):
        #administracion de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            user.persist(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()


    import logging


    @autobahn.wamp.register('users.profile.change_password')
    def changePassword(self, password, details):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            users = self.getUserId(ctx, details)
            logging.info(password)
            userId = users[0].id if len(users) > 0 else None
            logging.info(userId)
            r = UsersModel.changePassword(ctx, userId, password)
            ctx.con.commit()
            return r


        finally:
            ctx.closeConn()
