# -*- coding: utf-8 -*-
import inject, logging
import psycopg2

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config
from model.systems.digesto.digesto import Digesto


'''
    Clase de acceso mediante wamp a los métodos del digesto
'''
class WampDigesto(ApplicationSession):

    def __init__(self,config=None):
        logging.debug('instanciando WampDigesto')
        ApplicationSession.__init__(self, config)

        self.digesto = inject.instance(Digesto)
        self.serverConfig = inject.instance(Config)

    '''
    como referencia tambien se puede sobreeescribir el onConnect
    def onConnect(self):
        logging.debug('transport connected')
        self.join(self.config.realm)
    '''

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.createNormative_async,'digesto.server.digesto.createNormative')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)


    def createNormative(self,normative,status,visibility,relateds,file):
        con = self._getDatabase()
        try:
            self.digesto.createNormative(con,normative,status,visibility,relateds,file)
            con.commit()
        finally:
            con.close()

    @coroutine
    def createNormative_async(self,normative,status,visibility,relateds,file):
        try:
            loop = asyncio.get_event_loop()
            yield from loop.run_in_executor(None,self.createNormative,normative,status,visibility,relateds,file)

        except Exception as e:
            logging.exception(e)
            return None
