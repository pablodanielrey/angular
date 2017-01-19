# -*- coding: utf-8 -*-
import inject
import logging
import uuid
# import asyncio
# from asyncio import coroutine
# from autobahn.asyncio.wamp import ApplicationSession

from model.users.entities.user import User

# from model.exceptions import *

import autobahn
import wamp

class Users(wamp.SystemComponentSession):


    @autobahn.wamp.register('users.find_by_id')
    def findById(self, ids):
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
            return User.find(ctx)
        finally:
            ctx.closeConn()
