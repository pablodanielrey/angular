# -*- coding: utf-8 -*-
import inject
import json
import uuid
import re
import logging
import psycopg2
import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.config import Config
from model.users.users import Users
from model.credentials.credentials import UserPassword
from model.mail.mail import Mail
from model.systems.ingreso.ingreso import Ingreso

from model.exceptions import *


class IngresoWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        self.users = inject.instance(Users)
        self.serverConfig = inject.instance(Config)
        self.mail = inject.instance(Mail)
        self.credentials = inject.instance(UserPassword)
        self.ingreso = inject.instance(Ingreso)

    @coroutine
    def onJoin(self, details):
        yield from self.register(self.sendEmailConfirmation_async, 'ingreso.mails.sendEmailConfirmation')
        yield from self.register(self.confirmEmail_async, 'ingreso.mails.confirmEmail')
        yield from self.register(self.changePassword_async, 'ingreso.user.changePassword')
        yield from self.register(self.sendErrorMail_async, 'ingreso.mails.sendErrorMail')
        yield from self.register(self.sendFinalMail_async, 'ingreso.mails.sendFinalMail')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def changePassword(self, dni, password):
        """
            Crea la clave del usuario.
            Solo en el caso de que ya no exista previamente un usuario y clave.
        """
        con = self._getDatabase()
        try:
            creds = self.credentials.findCredentials(con, dni)
            if creds is not None:
                return False

            uuser = self.users.findUserByDni(con, dni)
            if uuser is None:
                return False

            user = {
                'user_id': uuser['id'],
                'username': dni,
                'password': password
            }
            self.credentials.createUserPassword(con, user)
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def changePassword_async(self, dni, password):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.changePassword, dni, password)
        return r

    def sendEmailConfirmation(self, name, lastname, eid):
        con = self._getDatabase()
        try:
            self.ingreso.sendEmailConfirmation(con, name, lastname, eid)
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def sendEmailConfirmation_async(self, name, lastname, eid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.sendEmailConfirmation, name, lastname, eid)
        return r

    def confirmEmail(self, eid, hash):
        con = self._getDatabase()
        try:
            r = self.ingreso.confirmEmail(con, eid, hash)
            con.commit()
            return r

        finally:
            con.close()

    @coroutine
    def confirmEmail_async(self, eid, hash):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.confirmEmail, eid, hash)
        return r

    def sendFinalMail(self, user, password, email):
        self.ingreso.sendFinalEmail(user, password, email)
        return True

    @coroutine
    def sendFinalMail_async(self, user, password, email):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.sendFinalMail, user, password, email)
        return r

    def sendErrorMail(self, error, names, dni, email, tel):
        self.ingreso.sendErrorEmail(error, names, dni, email, tel)
        return True

    @coroutine
    def sendErrorMail_async(self, error, names, dni, email, tel):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.sendErrorMail, error, names, dni, email, tel)
        return r
