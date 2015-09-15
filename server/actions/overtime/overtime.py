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
        yield from self.register(self.getOvertimeRequests_async, 'overtime.getOvertimeRequests')
        yield from self.register(self.getOvertimeRequestsToManage_async, 'overtime.getOvertimeRequestsToManage')



    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)


    '''
     ' Obtener requerimientos de horas extra
     ' @param usersIds Lista de usuarios, si es una lista vacia retorna todos los usuarios
     ' @param states Lista de estados, si es una lista vacia retorna todos los estados
     '      [APPROVED, PENDING, REJECTED]'
     '''
    def getOvertimeRequests(self, usersIds, states):
        con = self._getDatabase()
        try:
            requests = self.overtime.getOvertimeRequests(con,states,None,usersIds)
            return requests

        finally:
            con.close()

    @coroutine
    def getOvertimeRequests_async(self, usersIds, states):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOvertimeRequests, usersIds, states)
        return r


    '''
     ' Obtener requerimientos de horas extra para administrar
     ' @param usersId Id de usuario
     ' @param states Lista con el estado estado de las solicitudes a consultar
     '      [APPROVED, PENDING, REJECTED]'
     ' @param group Grupo (Oficinas)
     '      ROOT|TREE --> ROOT = oficinas directas, TREE = oficinas directas y todas las hijas
     '''
    def getOvertimeRequestsToManage(self, userId, states, group):
        con = self._getDatabase()
        try:            
            requests = self.overtime.getOvertimeRequestsToManage(con, userId, states, group)
            return requests

        finally:
            con.close()

    @coroutine
    def getOvertimeRequestsToManage_async(self,userId, states=[], group='ROOT'):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOvertimeRequestsToManage, userId, states, group)
        return r
