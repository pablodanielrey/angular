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
        yield from self.register(self.requestOvertime_async, 'overtime.requestOvertime')
        yield from self.register(self.updateStatus_async, 'overtime.updateStatus')
        yield from self.register(self.getMinutesApproved_async, 'overtime.getMinutesApproved')



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



    '''
     ' Solicitar requerimiento de horas extra
     ' @param requestorId Id de usuario que solicita el requerimiento
     ' @param userId Id del usuario para quien se solicita el requerimiento
     ' @param begin Fecha y hora de inicio de solicitud
     ' @param end Fecha y hora de fin de la solicitud
     ' @param reason Razon de la solicitud
     '''
    def requestOvertime(self, requestorId, userId, begin, end, reason):
        con = self._getDatabase()
        try:
            overtimeId = self.overtime.requestOvertime(con, requestorId, userId, begin, end, reason)
            con.commit()
            return overtimeId

        finally:
            con.close()

    @coroutine
    def requestOvertime_async(self, requestorId, userId, begin, end, reason):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.requestOvertime, requestorId, userId, begin, end, reason)
        return r



    '''
     ' Actualizar estado de overtime
     ' @param userId Id del usuario quien solicita el cambio de estado
     ' @param requestId Id del requerimiento de hora extra
     ' @param status Nuevo estado
     '''
    def updateStatus(self, userId, requestId, status):
        con = self._getDatabase()
        try:
            events = self.overtime.updateOvertimeRequestStatus(con, userId, requestId, status)
            con.commit()
            return events

        finally:
            con.close()

    @coroutine
    def updateStatus_async(self, userId, requestId, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.updateStatus, userId, requestId, status)
        return r
        

    '''
     ' Obtener cantidad de minutos de los requerimientos de horas extras aprobadas por usuario
     ' @param userId Id del usuario del cual se desea saber las horas extras aprobadas
     ' @param begin Fecha de inicio de la solicitud
     ' @param begin Fecha de fin de la solicitud
     '''
    def getMinutesApproved(self, userId, begin, end):
        con = self._getDatabase()
        try:
            requests = self.overtime.getOvertimeRequests(con, ['APPROVED'], None, [userId], begin, end)
            minutes = 0
            for request in requests:              
              minutes += (request['end'] - request['begin']).seconds / 60
            return minutes              

        finally:
            con.close()
        
        
    @coroutine
    def getMinutesApproved_async(self, userId, begin, end = None):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getMinutesApproved, userId, begin, end)
        return r        
