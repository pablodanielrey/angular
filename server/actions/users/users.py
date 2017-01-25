# -*- coding: utf-8 -*-
import inject
import logging
import uuid
# import asyncio
# from asyncio import coroutine
# from autobahn.asyncio.wamp import ApplicationSession

from model.users.entities.user import User
from model.users.entities.user import Telephone
from model.users.entities.mail import Mail



# from model.exceptions import *

import autobahn
import wamp

class Users(wamp.SystemComponentSession):

    @autobahn.wamp.register('users.search')
    def search(self, search):
        #busqueda de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return User.search(ctx, search).values

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.admin')
    def admin(self, id):
        #administracion de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            user = None
            if id is not None:
                user = User.findById(ctx, id)

            if user is None:
                user = User()

            return user
        finally:
            ctx.closeConn()


    @autobahn.wamp.register('users.find_emails_by_user_id')
    def findEmailsByUserId(self, userId):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return Mail.find(ctx, userId=userId).fetch(ctx)

        finally:
            ctx.closeConn()




    @autobahn.wamp.register('users.add_email')
    def addMail(self, email):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            email.persist(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.delete_email')
    def deleteEmail(self, email):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            email.delete(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()


    @autobahn.wamp.register('users.send_confirm_email')
    def sendConfirmationMail(self, emailId):
        """
            envío el email para poder confirmar
        """
        pass

    @autobahn.wamp.register('users.confirm_email')
    def confirmMail(self, emailId, code):
        """
            chequeo el codigo de verificación y confirmo el email en caso de ser correcto.
            lo hace el modelo a esto.
        """
        pass

    @autobahn.wamp.register('users.admin_confirm_email')
    def adminConfirmMail(self, emailId):
        """
            confirmo el correo sin importar que codigo tiene.
            solo lo deberia ejecutar el administrador. perfiles se chequean en el modelo. despues cuando termine lo del login.
            no hacerlo todavia.
        """
        pass



    @autobahn.wamp.register('users.persist')
    def persist(self, user):
        #administracion de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            user.persist(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()




    @autobahn.wamp.register('users.find_by_ids')
    def findByIds(self, ids):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return User.findByIds(ctx, ids)

        finally:
            ctx.closeConn()


    @autobahn.wamp.register('users.find_by_dni')
    def findByDni(self, dnis):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return User.find(ctx, dni=dnis)
        finally:
            ctx.closeConn()


    @autobahn.wamp.register('users.find_photo')
    def findPhoto(self, pid):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return User.findPhoto(ctx, pid)
        finally:
            ctx.closeConn()

    @autobahn.wamp.register('users.find_photos')
    def findPhotos(self, users):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return User.findPhotos(ctx, users)
        finally:
            ctx.closeConn()


    @autobahn.wamp.register('users.find_all')
    def findAll(self):
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return User.find(ctx).values
        finally:
            ctx.closeConn()
