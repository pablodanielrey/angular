# -*- coding: utf-8 -*-
import inject
import re
import psycopg2
import time
import logging

from model.exceptions import *

from model.config import Config
from model.profiles import Profiles
from model.events import Events
from model.users.users import Users
from model.mail.mail import Mail

from model.systems.assistance.assistance import Assistance
from model.systems.assistance.date import Date
from model.systems.assistance.justifications.justifications import Justifications
from model.systems.offices.offices import Offices

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession


class JustificationsWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.date = inject.attr(Date)
        self.events = inject.attr(Events)
        self.mail = inject.attr(Mail)
        self.users = inject.attr(Users)
        self.offices = inject.attr(Offices)
        self.justifications = inject.attr(Justifications)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')

        yield from self.register(self.getJustificationsRequestsToManage_async, 'assistance.justifications.getJustificationsRequestsToManage')


        yield from self.register(self.getSpecialJustifications_async, 'assistance.justifications.getSpecialJustifications')





    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def getJustifications(self):
        con = self._getDatabase()
        try:
            ''' .... codigo aca ... '''
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def getJustifications_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getJustifications)
        return r



