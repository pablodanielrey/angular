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
        yield from self.register(self.getEconoPageDataUser_async,'sileg.getEconoPageDataUser')
        yield from self.register(self.getEconoPageDataPlace_async,'sileg.getEconoPageDataPlace')
        



        ##### positions #####
        yield from self.register(self.findPositionsByIds_async,'sileg.findPositionsByIds')
        yield from self.register(self.findPositionsAll_async,'sileg.findPositionsAll')
        
                
        
        ##### places #####
        yield from self.register(self.findPlacesByIds_async,'sileg.findPlacesByIds')
        yield from self.register(self.findPlacesAll_async,'sileg.findPlacesAll')
        
        
        
        ##### users #####
        yield from self.register(self.findUsersByIds_async,'sileg.findUsersByIds')
        
        
        
        ##### designations #####
        yield from self.register(self.findDesignationsByIds_async,'sileg.findDesignationsByIds')
        yield from self.register(self.findDesignationsBySearch_async,'sileg.findDesignationsBySearch')
        yield from self.register(self.persistDesignation_async,'sileg.persistDesignation')
        
        
   

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
        
               
    def findDesignationsByIds(self, ids):
        con = self.conn.get()
        try:
            return self.sileg.findDesignationsByIds(con, ids)
        finally:
            self.conn.put(con)

    @coroutine
    def findDesignationsByIds_async(self, ids):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findDesignationsByIds, ids)
        return r
        
        
        
        
        
        
        
    ##### find designations by search #####
    def findDesignationsBySearch(self, search):
        con = self.conn.get()
        try:
            return self.sileg.findDesignationsBySearch(con, search)
        finally:
            self.conn.put(con)

    @coroutine
    def findDesignationsBySearch_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findDesignationsBySearch, search)
        return r
        
        
        
    ##### find users by ids #####
    def findUsersByIds(self, ids):
        con = self.conn.get()
        try:
            return self.sileg.findUsersByIds(con, ids)
        finally:
            self.conn.put(con)

    @coroutine
    def findUsersByIds_async(self, ids):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findUsersByIds, ids)
        return r        
        
        
        
    ##### find places by ids #####
    def findPlacesByIds(self, ids):
        con = self.conn.get()
        try:
            return self.sileg.findPlacesByIds(con, ids)
        finally:
            self.conn.put(con)

    @coroutine
    def findPlacesByIds_async(self, ids):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findPlacesByIds, ids)
        return r
        
        
        
    ##### find positions by ids #####
    def findPositionsByIds(self, ids):
        con = self.conn.get()
        try:
            return self.sileg.findPositionsByIds(con, ids)
        finally:
            self.conn.put(con)

    @coroutine
    def findPositionsByIds_async(self, ids):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findPositionsByIds, ids)
        return r
        
        
        
    ##### find positions all #####
    def findPositionsAll(self):
        con = self.conn.get()
        try:
            return self.sileg.findPositionsAll(con)
        finally:
            self.conn.put(con)

    @coroutine
    def findPositionsAll_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findPositionsAll)
        return r

    ##### persist designation #####
    def persistDesignation(self, designation):
        con = self.conn.get()
        try:
            return self.sileg.persistDesignation(con, designation)
        finally:
            self.conn.put(con)

    @coroutine
    def persistDesignation_async(self, designation):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistDesignation, designation)
        return r                
        
        
        
        
        
    ##### find places all #####
    def findPlacesAll(self):
        con = self.conn.get()
        try:
            return self.sileg.findPlacesAll(con)
        finally:
            self.conn.put(con)

    @coroutine
    def findPlacesAll_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findPlacesAll)
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
        
