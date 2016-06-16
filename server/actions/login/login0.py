# -*- coding: utf-8 -*-
import inject
import logging

from model.login.login import Login
from model.login.session import SessionDAO
from model.profiles import Profiles

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
        #self.profiles = inject.instance(Profiles)
        self.profiles = None
        self.session = inject.instance(Session)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.login_async, 'system.login')
        yield from self.register(self.logout_async, 'system.logout')
        yield from self.register(self.validateSession_async, 'system.session.validate')
        #yield from self.register(self.generateResetPasswordHash_async, 'system.password.generateResetPasswordHash')
        #yield from self.register(self.changePassword_async, 'system.password.changePassword')
        #yield from self.register(self.changePasswordWithHash_async, 'system.password.changePasswordWithHash')
        #yield from self.register(self.checkProfileAccess_async, 'system.profiles.checkProfileAccess')

    '''
        Chequea que el usuario logeado en la sesion sid tenga alguno de los perfiles enviados en la lista de perfiles
    '''
    def checkProfileAccess(self, sid, roles):
        con = self.conn.get()
        try:
            r = self.profiles._checkAccessWithCon(con, sid, roles)
            return r

        finally:
            self.conn.put(con)

    '''
        valida que la session sid exista
    '''
    def validateSession(self, sid):
        con = self.conn.get()
        try:
            if len(self.session.findById(con, [sid])) > 0:
                return True
            else
                return False

        except Exception as e:
            logging.exception(e)
            return False

        finally:
            self.conn.put(con)

    '''
        Genera el hash para reseteo de la clave
    '''
    def generateResetPasswordHash(self, username):
        con = self.conn.get()
        try:
            hash = self.loginModel.generateResetPasswordHash(con, username)
            con.commit()
            return hash

        except Exception as e:
            logging.exception(e)
            return None

        finally:
            self.conn.put(con)

    '''
        cambia la clave del usuario determinado por el hash pasado como parámetro
    '''
    def changePassword(self, sid, username, password):
        con = self.conn.get()
        try:
            r = self.loginModel.changePassword(con, sid, username, password)
            con.commit()
            return r

        except Exception as e:
            logging.exception(e)
            return False

        finally:
            self.conn.put(con)

    '''
        cambia la clave del usuario determinado por el hash pasado como parámetro
    '''
    def changePasswordWithHash(self, username, password, hhash):
        con = self.conn.get()
        try:
            r = self.loginModel.changePasswordWithHash(con, username, password, hhash)
            con.commit()
            return r

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
    def generateResetPasswordHash_async(self, username):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.generateResetPasswordHash, username)
        return r

    @coroutine
    def changePasswordWithHash_async(self, username, password, hash):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.changePasswordWithHash, username, password, hash)
        return r

    @coroutine
    def changePassword_async(self, sid, username, password):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.changePassword, sid, username, password)
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
    def checkProfileAccess_async(self, sid, roles):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.checkProfileAccess, sid, roles)
        return r

    @coroutine
    def validateSession_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.validateSession, sid)
        return r
