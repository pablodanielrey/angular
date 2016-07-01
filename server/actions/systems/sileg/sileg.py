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
        yield from self.register(self.getCathedras_async,'sileg.getCathedras')
        yield from self.register(self.getUsers_async,'sileg.getUsers')
        yield from self.register(self.getDesignationFull_async,'sileg.getDesignationFull')
        yield from self.register(self.getEconoPageDataUser_async,'sileg.getEconoPageDataUser')
        yield from self.register(self.getEconoPageDataPlace_async,'sileg.getEconoPageDataPlace')
        
        
   

    def getCathedras(self):
        con = self.conn.get()
        try:
            return self.sileg.getCathedras(con)
        finally:
            self.conn.put(con)

    @coroutine
    def getCathedras_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getCathedras)
        return r
 

    def getUsers(self):
        con = self.conn.get()
        try:
            return self.sileg.getUsers(con)
        finally:
            self.conn.put(con)

    @coroutine
    def getUsers_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getUsers)
        return r
        
               
    def getDesignationFull(self, id):
        con = self.conn.get()
        try:
            return self.sileg.getDesignationFull(con, id)
        finally:
            self.conn.put(con)

    @coroutine
    def getDesignationFull_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getDesignationFull, id)
        return r
        
                       
        
    def getEconoPageDataUser(self, userId):
        con = self.conn.get()
        try:
            return self.sileg.getEconoPageDataUser(con, userId)
        finally:
            self.conn.put(con)
        
    @coroutine
    def getEconoPageDataUser_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getEconoPageDataUser, userId)
        return r
        
        
    def getEconoPageDataPlace(self, placeId):
        con = self.conn.get()
        try:
            return self.sileg.getEconoPageDataPlace(con, placeId)
        finally:
            self.conn.put(con)
        
    @coroutine
    def getEconoPageDataPlace_async(self, placeId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getEconoPageDataPlace, placeId)
        return r        
        
