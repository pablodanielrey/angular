# -*- coding: utf-8 -*-
import inject
import logging

from model.users.users import User, Mail
from model.login.login import Login, ResetPassword
from model.login.session import Session
from model.registry import Registry
from model.connection import connection

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


    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.login_async, 'system.login')
        yield from self.register(self.logout_async, 'system.logout')
        yield from self.register(self.testUser_async, 'system.testUser')
        yield from self.register(self.validateSession_async, 'system.session.validate')
        yield from self.register(self.hasOneRole_async, 'system.profile.hasOneRole')

        yield from self.register(self.findByDni_async, 'system.login.findByDni')
        yield from self.register(self.checkCode_async, 'system.login.checkCode')
        yield from self.register(self.changePassword_async, 'system.login.changePassword')


    def changePassword(self, uid, dni, eid, code, passw):
        con = self.conn.get()
        try:
            ok = ResetPassword.resetPassword(con, uid, dni, eid, code, passw)
            con.commit()
            return ok

        finally:
            self.conn.put(con)

    @coroutine
    def changePassword_async(self, uid, dni, eid, code, passw):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.changePassword, uid, dni, eid, code, passw)
        return r

    def checkCode(self, eid, code):
        con = self.conn.get()
        try:
            return ResetPassword.checkEmailCode(con, eid, code);

        finally:
            self.conn.put(con)

    @coroutine
    def checkCode_async(self, eid, code):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.checkCode, eid, code)
        return r

    def findByDni(self, dni):
        con = self.conn.get()
        try:
            data = ResetPassword.findByDni(con, dni)
            con.commit()
            return data

        finally:
            self.conn.put(con)

    @coroutine
    def findByDni_async(self, dni):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findByDni, dni)
        return r

    def testUser(self, username):
        con = self.conn.get()
        try:
            return self.loginModel.testUser(con, username)

        finally:
            self.conn.put(con)

    '''
        valida que la session sid exista
    '''
    def validateSession(self, sid):
        con = self.conn.get()
        try:
            self.loginModel.touch(con, sid)
            con.commit()
            return True

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
            s = self.loginModel.login(con, username, password)
            con.commit()
            return s.__dict__

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

    '''
        Verifica que tenga al menos un rol
    '''
    def hasOneRole(self, sid, roles= []):
        con = self.conn.get()
        try:
            return self.loginModel.hasOneRole(con, sid, roles)

        except Exception as e:
            logging.exception(e)
            return False

        finally:
            self.conn.put(con)

    @coroutine
    def testUser_async(self, username):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.testUser, username)
        return r

    @coroutine
    def hasOneRole_async(self, sid, roles):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.hasOneRole, sid, roles)
        return r

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
