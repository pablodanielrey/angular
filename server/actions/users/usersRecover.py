# -*- coding: utf-8 -*-
import inject
import logging
import uuid
# import asyncio
# from asyncio import coroutine
# from autobahn.asyncio.wamp import ApplicationSession

from model.users.usersModel import UsersModel
from model.users.entities.user import User
from model.users.entities.mail import Mail

# from model.exceptions import *

import autobahn
import wamp

class UsersRecover(wamp.SystemComponentSession):

    @autobahn.wamp.register('users.recover.send_code_by_dni')
    def sendCodeByDni(self, dni):
        #busqueda de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            user = User.find(ctx, dni=dni).fetch(ctx)
            if not len(user):
                return False

            #TODO: Enviar codigo por email

            return user

        finally:
            ctx.closeConn()
