# -*- coding: utf-8 -*-
import psycopg2
import inject
import logging

from model.config import Config
from model.login import Login

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession


class LoginWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.login = inject.instance(Login)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.login_async, 'system.login')
        yield from self.register(self.logout_async, 'system.logout')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    '''
        Loguea al usuario dentro del sistema y genera una sesion
    '''
    def login(self, username, password, info=None):
        con = self._getDatabase()
        try:
            return self.login.login(username, password)

        except Exception as e:
            logging.exception(e)
            return None

        finally:
            con.close()

    @coroutine
    def login_async(self, username, password, info=None):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.login, username, password, info)
        return r

    '''
        Elimina la sesion de usuario identificada por sid
    '''
    def logout(self, sid):
        con = self._getDatabase()
        try:
            self.login.logout(con, sid)
            con.commit()
            return True

        except Exception as e:
            logging.exception(e)
            return False

        finally:
            con.close()

    @coroutine
    def logout_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.logout, sid)
        return r
