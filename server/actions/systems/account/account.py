# -*- coding: utf-8 -*-
import inject
import json
import re
import logging
import psycopg2
import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.registry import Registry
from model.connection.connection import Connection

from model.account.account import AccountModel
from model.login.login import Login

class AccountWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        registry = inject.instance(Registry)
        self.reg = registry.getRegistry('dcsys')
        self.conn = Connection(self.reg)
        self.accountModel = inject.instance(AccountModel)
        self.loginModel = inject.instance(Login)

    @coroutine
    def onJoin(self, details):
        yield from self.register(self.deleteMail_async, 'account.deleteMail')
        yield from self.register(self.createUser_async, 'account.createUser')
        yield from self.register(self.findByDni_async, 'account.findByDni')
        yield from self.register(self.updateType_async, 'account.updateType')
        yield from self.register(self.getTypes_async, 'account.getTypes')


    '''
     ' Eliminacion de email
     ' @override id uuid del email
     '''
    def deleteMail(self, id):
        con = self.conn.get()
        try:
            self.accountModel.deleteMail(con, id)
            con.commit()
            return True
        finally:
            self.conn.put(con)

    @coroutine
    def deleteMail_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.deleteMail, id)
        return r

    def findByDni(self, sid, dni):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            return self.accountModel.findByDni(con, userId, dni)
        finally:
            self.conn.put(con)

    @coroutine
    def findByDni_async(self, sid, dni):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findByDni, sid, dni)
        return r

    def getTypes(self, sid):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            return self.accountModel.getTypes(con, userId)
        finally:
            self.conn.put(con)

    @coroutine
    def getTypes_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getTypes, sid)
        return r

    def updateType(self, sid, user, type):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            self.accountModel.updateType(con, userId, user, type)
            con.commit()
            return True
        finally:
            self.conn.put(con)

    @coroutine
    def updateType_async(self, sid, user, type):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.updateType, sid, user, type)
        return r

    def createUser(self, sid, user, studentNumber, type):
        '''
            user: {'dni': '1233487', 'lastname': 'pompin', 'name': 'pepe'}
            studentNumber : '111/1'
            type: 'student | teacher'
        '''
        con = self.conn.get()
        try:
            creatorId = self.loginModel.getUserId(con, sid)
            u = self.accountModel.createUser(con, creatorId, user, studentNumber, type)
            con.commit()
            return True

        finally:
           self.conn.put(con)

    @coroutine
    def createUser_async(self, sid, user, studentNumber, type):
       loop = asyncio.get_event_loop()
       r = yield from loop.run_in_executor(None, self.createUser, sid, user, studentNumber, type)
       return r
