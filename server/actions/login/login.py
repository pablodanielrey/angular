# -*- coding: utf-8 -*-
import inject
import logging

from model.login.login import Login
from model.login.session import SessionDAO
from model.registry import Registry
from model.connection import Connection

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession


class LoginWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        reg = inject.instance(Registry)
        self.conn = connection.Connection(reg.getRegistry('dcsys'))
        self.loginModel = inject.instance(Login)
        self.session = inject.instance(Session)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.login_async, 'system.login')
        yield from self.register(self.logout_async, 'system.logout')
        yield from self.register(self.validateSession_async, 'system.session.validate')

    '''
        valida que la session sid exista
    '''
    def validateSession(self, sid):
        con = self.conn.get()
        try:
            if len(self.session.findById(con, [sid])) > 0:
                return True
            else:
                return False

        except Exception as e:
            logging.exception(e)
            return False

        finally:
            self.conn.put(con)

    '''
        Loguea al usuario dentro del sistema y genera una sesion
    '''
    def login(self, username, password):
        con = self.conn.get()
        try:
            sid = self.loginModel.login(con, username, password)
            con.commit()
            return sid

        except Exception as e:
            logging.exception(e)
            return None

        finally:
            self.conn.put(con)

    '''
        Elimina la sesion de usuario identificada por sid
    '''
    def logout(self, sid):
        con = self.conn.get()
        try:
            self.loginModel.logout(con, sid)
            con.commit()
            return True

        except Exception as e:
            logging.exception(e)
            return False

        finally:
            self.conn.put(con)

    @coroutine
    def login_async(self, username, password):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.login, username, password)
        return r

    @coroutine
    def logout_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.logout, sid)
        return r

    @coroutine
    def validateSession_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.validateSession, sid)
        return r
