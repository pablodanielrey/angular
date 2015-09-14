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

from model.events import Events
from model.profiles import Profiles

from model.exceptions import *

from model.systems.assistance.overtime import Overtime




class OvertimeWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        self.serverConfig = inject.instance(Config)
        self.overtime = inject.instance(Overtime)



    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getOvertimeRequestsByUsers_async, 'overtime.getOvertimeRequestsByUsers')
        yield from self.register(self.getOvertimeRequestsByUsers_async, 'overtime.getOvertimeRequestsToManage')
        yield from self.register(self.getOvertimeRequestsByUsers_async, 'overtime.updateOvertimeRequestStatus')
        yield from self.register(self.getOvertimeRequestsByUsers_async, 'overtime.requestOvertime')


    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)


    '''
     ' Obtener requerimiento de overtime a partir de una una lista de usuarios
     '''
    def getOvertimeRequestsByUsers(self, users):
        con = self._getDatabase()
        try:
            requests = self.overtime.getOvertimeRequests(con,[],None,users)
            return requests

        finally:
            con.close()

    @coroutine
    def getOvertimeRequestsByUsers_async(self, users):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOvertimeRequestsByUsers, users)
        return r
