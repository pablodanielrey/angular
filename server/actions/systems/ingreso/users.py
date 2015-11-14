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
        yield from self.register(self.checkEmailCode_async, 'ingreso.mails.checkEmailCode')
        yield from self.register(self.sendErrorMail_async, 'ingreso.mails.sendErrorMail')
        yield from self.register(self.uploadIngresoData_async, 'ingreso.user.uploadIngresoData')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def uploadIngresoData(self, dni, password, user, email, eid, code):
        con = self._getDatabase()
        try:
            # genero una clave.
            apassword = 'Ya tiene registrado una clave'
            creds = self.credentials.findCredentials(con, dni)
            if creds is None:
                uuser = self.users.findUserByDni(con, dni)
                if uuser is None:
                    con.rollback()
                    return False

                cuser = {
                    'user_id': uuser['id'],
                    'username': dni,
                    'password': password
                }
                self.credentials.createUserPassword(con, cuser)
                apassword = password


            # confirmo el email
            r = self.ingreso.confirmEmail(con, eid, code)
            if not r:
                con.rollback()
                return False
            else:
                con.commit()

            # envío el email de finalización
            self.ingreso.sendFinalEmail(user, apassword, email)

            return True

        finally:
            con.close()

    @coroutine
    def uploadIngresoData_async(self, dni, password, user, email, eid, code):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.uploadIngresoData, dni, password, user, email, eid, code)
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

    def checkEmailCode(self, eid, hash):
        con = self._getDatabase()
        try:
            r = self.ingreso.checkEmailCode(con, eid, hash)
            return r

        finally:
            con.close()

    @coroutine
    def checkEmailCode_async(self, eid, hash):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.checkEmailCode, eid, hash)
        return r

    def sendErrorMail(self, error, names, dni, email, tel):
        self.ingreso.sendErrorEmail(error, names, dni, email, tel)
        return True

    @coroutine
    def sendErrorMail_async(self, error, names, dni, email, tel):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.sendErrorMail, error, names, dni, email, tel)
        return r
