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

    @autobahn.wamp.register('users.profile.send_email_confirmation')
    def sendEmailConfirmation(self, userId, eid, details):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            logging.warn('userId: {} sendEmailConfirmation {}'.format(userId,eid))
            UsersModel.sendEmailConfirmation(ctx, userId, eid)
            ctx.con.commit()

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.profile.process_code')
    def processCode(self, emailId, code, details):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            emails = Mail.findByIds(ctx, [emailId])
            if len(emails) <= 0:
                raise Exception('No existe el correo')
            if code != emails[0].hash:
                raise Exception('Código incorrecto')

            emails[0].confirmed = True
            emails[0].persist(ctx)
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
