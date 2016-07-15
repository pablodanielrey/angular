# -*- coding: utf-8 -*-
import inject, logging
import psycopg2

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.registry.registry import Registry
from model.connection.connection import connection
from model.myfirstsystem.MyFirstSystem import MyFirstSystem




class MyFirstSystemWamp(ApplicationSession):

    """
      Interface entre el cliente y el servidor
    """

    def __init__(self,config=None):
        ApplicationSession.__init__(self, config)
        reg = inject.instance(Registry)
        self.conn = connection.Connection(reg.getRegistry('myfirstsystem'))
        self.myFirstSystem = inject.instance(MyFirstSystem)


    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getMessage_async, 'myfirstsystem.getMessage')
        yield from self.register(self.helloWorld_async, 'myfirstsystem.helloWorld')


    ##### getMessage #####
    def getMessage(self):
        con = self.conn.get()
        try:
            return self.myFirstSystem.getMessage(con)
        finally:
            self.conn.put(con)

    @coroutine
    def getMessage_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getMessage)
        return r




    ##### helloWorld #####
    def helloWorld(self, param1, param2):
        con = self.conn.get()
        try:
            return self.myFirstSystem.helloWorld(con, param1, param2)
        finally:
            self.conn.put(con)

    @coroutine
    def helloWorld_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.helloWorld, param1, param2)
        return r
