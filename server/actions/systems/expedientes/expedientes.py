# -*- coding: utf-8 -*-

import inject, asyncio, psycopg2
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config

from model.systems.expedientes.Destino import Destino
from model.systems.expedientes.Expediente import Expediente
from model.systems.expedientes.Lugar import Lugar
from model.systems.expedientes.Nota import Nota
from model.systems.expedientes.Participacion import Participacion
from model.systems.expedientes.Persona import Persona
from model.systems.expedientes.Tema import Tema

class ExpedientesWamp(ApplicationSession):
    
    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        
        self.serverConfig = inject.instance(Config)

        self.destino = inject.instance(Destino)
        self.expediente = inject.instance(Expediente)
        self.lugar = inject.instance(Lugar)
        self.nota = inject.instance(Nota)
        self.participacion = inject.instance(Participacion)
        self.persona = inject.instance(Persona)
        self.tema = inject.instance(Tema)

    @coroutine
    def onJoin(self, details):

        yield from self.register(self.getDestinoById_async, 'expedientes.getDestinoById')
        yield from self.register(self.getDestinoGridData_async, 'expedientes.getDestinoGridData')
        yield from self.register(self.numRowsDestino_async, 'expedientes.destino.numRows')  
        yield from self.register(self.getExpedienteById_async, 'expedientes.getExpedienteById')
        yield from self.register(self.getExpedienteGridData_async, 'expedientes.getExpedienteGridData')
        yield from self.register(self.numRowsExpediente_async, 'expedientes.expediente.numRows')  
        yield from self.register(self.getLugarById_async, 'expedientes.getLugarById')
        yield from self.register(self.getLugarGridData_async, 'expedientes.getLugarGridData')
        yield from self.register(self.numRowsLugar_async, 'expedientes.lugar.numRows')  
        yield from self.register(self.getNotaById_async, 'expedientes.getNotaById')
        yield from self.register(self.getNotaGridData_async, 'expedientes.getNotaGridData')
        yield from self.register(self.numRowsNota_async, 'expedientes.nota.numRows')  
        yield from self.register(self.getParticipacionById_async, 'expedientes.getParticipacionById')
        yield from self.register(self.getParticipacionGridData_async, 'expedientes.getParticipacionGridData')
        yield from self.register(self.numRowsParticipacion_async, 'expedientes.participacion.numRows')  
        yield from self.register(self.getPersonaById_async, 'expedientes.getPersonaById')
        yield from self.register(self.getPersonaGridData_async, 'expedientes.getPersonaGridData')
        yield from self.register(self.numRowsPersona_async, 'expedientes.persona.numRows')  
        yield from self.register(self.getTemaById_async, 'expedientes.getTemaById')
        yield from self.register(self.getTemaGridData_async, 'expedientes.getTemaGridData')
        yield from self.register(self.numRowsTema_async, 'expedientes.tema.numRows')  

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    @coroutine
    def getDestinoById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getDestinoById, id)
        return r

    def getDestinoById(self, id):
        con = self._getDatabase()
        try:
            r = self.destino.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def getDestinoGridData_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getDestinoGridData, search)
        return r

    def getDestinoGridData(self, search):
        con = self._getDatabase()
        try:
            r = self.destino.gridData(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def numRowsDestino_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.numRowsDestino, search)
        return r

    def numRowsDestino(self, search):
        con = self._getDatabase()
        try:
            r = self.destino.numRows(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def getExpedienteById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getExpedienteById, id)
        return r

    def getExpedienteById(self, id):
        con = self._getDatabase()
        try:
            r = self.expediente.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def getExpedienteGridData_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getExpedienteGridData, search)
        return r

    def getExpedienteGridData(self, search):
        con = self._getDatabase()
        try:
            r = self.expediente.gridData(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def numRowsExpediente_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.numRowsExpediente, search)
        return r

    def numRowsExpediente(self, search):
        con = self._getDatabase()
        try:
            r = self.expediente.numRows(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def getLugarById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getLugarById, id)
        return r

    def getLugarById(self, id):
        con = self._getDatabase()
        try:
            r = self.lugar.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def getLugarGridData_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getLugarGridData, search)
        return r

    def getLugarGridData(self, search):
        con = self._getDatabase()
        try:
            r = self.lugar.gridData(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def numRowsLugar_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.numRowsLugar, search)
        return r

    def numRowsLugar(self, search):
        con = self._getDatabase()
        try:
            r = self.lugar.numRows(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def getNotaById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getNotaById, id)
        return r

    def getNotaById(self, id):
        con = self._getDatabase()
        try:
            r = self.nota.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def getNotaGridData_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getNotaGridData, search)
        return r

    def getNotaGridData(self, search):
        con = self._getDatabase()
        try:
            r = self.nota.gridData(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def numRowsNota_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.numRowsNota, search)
        return r

    def numRowsNota(self, search):
        con = self._getDatabase()
        try:
            r = self.nota.numRows(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def getParticipacionById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getParticipacionById, id)
        return r

    def getParticipacionById(self, id):
        con = self._getDatabase()
        try:
            r = self.participacion.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def getParticipacionGridData_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getParticipacionGridData, search)
        return r

    def getParticipacionGridData(self, search):
        con = self._getDatabase()
        try:
            r = self.participacion.gridData(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def numRowsParticipacion_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.numRowsParticipacion, search)
        return r

    def numRowsParticipacion(self, search):
        con = self._getDatabase()
        try:
            r = self.participacion.numRows(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def getPersonaById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getPersonaById, id)
        return r

    def getPersonaById(self, id):
        con = self._getDatabase()
        try:
            r = self.persona.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def getPersonaGridData_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getPersonaGridData, search)
        return r

    def getPersonaGridData(self, search):
        con = self._getDatabase()
        try:
            r = self.persona.gridData(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def numRowsPersona_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.numRowsPersona, search)
        return r

    def numRowsPersona(self, search):
        con = self._getDatabase()
        try:
            r = self.persona.numRows(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def getTemaById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getTemaById, id)
        return r

    def getTemaById(self, id):
        con = self._getDatabase()
        try:
            r = self.tema.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def getTemaGridData_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getTemaGridData, search)
        return r

    def getTemaGridData(self, search):
        con = self._getDatabase()
        try:
            r = self.tema.gridData(con, search)
            return r

        finally:
            con.close()

    @coroutine
    def numRowsTema_async(self, search):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.numRowsTema, search)
        return r

    def numRowsTema(self, search):
        con = self._getDatabase()
        try:
            r = self.tema.numRows(con, search)
            return r

        finally:
            con.close()

