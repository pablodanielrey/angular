# -*- coding: utf-8 -*-
import inject
import json
import uuid
import re
import logging
import psycopg2
import hashlib
import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.config import Config
from model.users.users import Users
from model.events import Events
from model.profiles import Profiles

from model.exceptions import *


class UsersWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        self.users = inject.instance(Users)
        self.serverConfig = inject.instance(Config)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.findById_async, 'users.findById')
        yield from self.register(self.persistUser_async, 'users.persistUser')
        yield from self.register(self.listUsers_async, 'users.listUsers')
        yield from self.register(self.findUsersIds_async, 'users.findUsersIds')
        yield from self.register(self.findUsersByIds_async, 'users.findUsersByIds')
        yield from self.register(self.findMails_async, 'users.mails.findMails')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def findById(self, id):
        con = self._getDatabase()
        try:
            data = self.users.findUser(con, id)
            return data

        finally:
            con.close()

    @coroutine
    def findById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findById, id)
        return r


    '''
     ' Persistir usuario
     ' Si el id esta definido se actualiza caso contrario se inserta
     ' @param user Diccionario con los datos de usuario
     '    dni
     '    name
     '    lastname
     '    city
     '    country
     '    adress
     '    genre
     '    birthdate
     '    residence_city
     '    version
     '''
    def persistUser(self, user):
        con = self._getDatabase()
        try:
            if 'id' not in user or not user['id']:
                userId = self.users.createUser(con, user)
            else:
                self.users.updateUser(con, user)
                userId = user['id']

            con.commit()
            return userId

        finally:
            con.close()

    @coroutine
    def persistUser_async(self, user):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistUser, user)
        return r


    '''
     ' Listar usuarios
     '''
    def listUsers(self):
        con = self._getDatabase()
        try:
            users = self.users.listUsers(con)
            return users

        finally:
            con.close()

    @coroutine
    def listUsers_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.listUsers)
        return r


    def findUsersIds(self):
        con = self._getDatabase()
        try:
            # codigo
            con.commit()
            return []

        finally:
            con.close()

    @coroutine
    def findUsersIds_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findUsersIds)
        return r




    def findUsersByIds(self, ids):
        con = self._getDatabase()
        try:
            # codigo
            con.commit()
            return []

        finally:
            con.close()

    @coroutine
    def findUsersByIds_async(self, ids):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findUsersByIds, ids)
        return r



    '''
     ' Buscar mails a partir de un userId
     '''
    def findMails(self, userId):
        con = self._getDatabase()
        try:
            mails = self.users.listMails(con, userId)
            return mails

        finally:
            con.close()

    @coroutine
    def findMails_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findMails, userId)
        return r
