# -*- coding: utf-8 -*-
import psycopg2
import inject
import logging

from model.config import Config
from model.login import Login
from model.profiles import Profiles
from model.session import Session

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession


class LoginWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.loginModel = inject.instance(Login)
        self.profiles = inject.instance(Profiles)
        self.session = inject.instance(Session)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.login_async, 'system.login')
        yield from self.register(self.logout_async, 'system.logout')
        yield from self.register(self.validateSession_async, 'system.session.validate')
        yield from self.register(self.generateResetPasswordHash_async, 'system.password.generateResetPasswordHash')
        yield from self.register(self.changePasswordWithHash_async, 'system.password.changePasswordWithHash')
        yield from self.register(self.checkProfileAccess_async, 'system.profiles.checkProfileAccess')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    '''
        Chequea que el usuario logeado en la sesion sid tenga alguno de los perfiles enviados en la lista de perfiles
    '''
    def checkProfileAccess(self, sid, roles):
        con = self._getDatabase()
        try:
            r = self.profiles._checkAccessWithCon(con, sid, roles)
            return r

        finally:
            con.close()

    '''
        valida que la session sid exista
    '''
    def validateSession(self, sid):
        con = self._getDatabase()
        try:
            self.session._findSession(con, sid)
            return True

        except Exception as e:
            logging.exception(e)
            return False

        finally:
            con.close()

    '''
        Genera el hash para reseteo de la clave
    '''
    def generateResetPasswordHash(self, username):
        con = self._getDatabase()
        try:
            hash = self.loginModel.generateResetPasswordHash(con, username)
            con.commit()
            return hash

        except Exception as e:
            logging.exception(e)
            return None

        finally:
            con.close()

    '''
        cambia la clave del usuario determinado por el hash pasado como parámetro
    '''
    def changePasswordWithHash(self, username, password, hash):
        con = self._getDatabase()
        try:
            r = self.loginModel.changePasswordWithHash(con, username, password, hash)
            con.commit()
            return r

        except Exception as e:
            logging.exception(e)
            return False

        finally:
            con.close()

    '''
        Loguea al usuario dentro del sistema y genera una sesion
    '''
    def login(self, username, password):
        con = self._getDatabase()
        try:
            return self.loginModel.login(con, username, password)

        except Exception as e:
            logging.exception(e)
            return None

        finally:
            con.close()

    '''
        Elimina la sesion de usuario identificada por sid
    '''
    def logout(self, sid):
        con = self._getDatabase()
        try:
            self.loginModel.logout(con, sid)
            con.commit()
            return True

        except Exception as e:
            logging.exception(e)
            return False

        finally:
            con.close()

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
