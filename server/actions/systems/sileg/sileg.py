# -*- coding: utf-8 -*-
import inject, logging
import psycopg2

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.registry import Registry
from model.connection import connection
from model.sileg.sileg import SilegModel

'''
    Clase de acceso mediante wamp a los métodos del sileg
'''
class SilegWamp(ApplicationSession):

    def __init__(self,config=None):
        logging.debug('instanciando WampDigesto')
        ApplicationSession.__init__(self, config)
        reg = inject.instance(Registry)
        
        self.conn = connection.Connection(reg.getRegistry('dcsys2'))

        self.sileg = inject.instance(SilegModel)



    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getPlaceById_async,'sileg.getPlaceById')

   

    def getPlaceById(self,ids):
        con = self.conn.get()
        try:
            return self.sileg.getPlaceById(con, ids)
        finally:
            self.conn.put(con)

    @coroutine
    def getPlaceById_async(self, ids):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getPlaceById, ids)
        return r
        
