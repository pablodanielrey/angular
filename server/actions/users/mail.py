# -*- coding: utf-8 -*-
import inject
import logging
import psycopg2
import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.config import Config
from model.users.users import Users
from model.mail.mail import Mail
from model.events import Events
from model.profiles import Profiles


class UserMailsWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.users = inject.attr(Users)
        self.events = inject.attr(Events)
        self.profiles = inject.attr(Profiles)
        self.mails = inject.attr(Mail)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.deleteMail_async, 'users.mails.deleteMail')
        yield from self.register(self.confirmMail_async, 'users.mails.confirmMail')
        yield from self.register(self.sendConfirmMail_async, 'users.mails.sendConfirmMail')
        yield from self.register(self.persistMail_async, 'users.mails.persistMail')
        yield from self.register(self.findMails_async, 'users.mails.findMails')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def deleteMail(self, id):
        con = self._getDatabase()
        try:
            email = self.users.findMail(con, id)
            if email is None:
                return True

            self.users.deleteMail(con, email['id'])
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def deleteMail_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.deleteMail, id)
        return r

    def confirmMail(self, hash):
        con = self._getDatabase()
        try:
            # codigo aca
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def confirmMail_async(self, hash):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.confirmMail, hash)
        return r

    def sendConfirmMail(self, id):
        con = self._getDatabase()
        try:
            # codigo aca
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def sendConfirmMail_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.sendConfirmMail, id)
        return r

    def persistMail(self, userId, email):
        con = self._getDatabase()
        try:
            # codigo aca
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def persistMail_async(self, userId, email):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistMail, userId, email)
        return r

    def findMails(self, userId):
        con = self._getDatabase()
        try:
            # codigo aca
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def findMails_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findMails, userId)
        return r
