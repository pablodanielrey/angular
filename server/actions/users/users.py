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
                if user is not None:
                    user.emails = Mail.find(ctx, userId=id).fetch(ctx)

            if user is None:
                user = User()
                user.emails = []

            return user
        finally:
            ctx.closeConn()



    @autobahn.wamp.register('users.persist')
    def persist(self, user):
        #administracion de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            user.persist(ctx)

            email = Mail()
            emailsToDelete = email.find(ctx, userId=user.id).fetch(ctx)
            for e in emailsToDelete:
                e.delete(ctx)

            for e in user.emails:
                e.userId = user.id
                e.persist(ctx)

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
