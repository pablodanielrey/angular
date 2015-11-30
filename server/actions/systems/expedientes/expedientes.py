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
        yield from self.register(self.getExpedienteById_async, 'expedientes.getExpedienteById')
        yield from self.register(self.getLugarById_async, 'expedientes.getLugarById')
        yield from self.register(self.getNotaById_async, 'expedientes.getNotaById')
        yield from self.register(self.getParticipacionById_async, 'expedientes.getParticipacionById')
        yield from self.register(self.getPersonaById_async, 'expedientes.getPersonaById')
        yield from self.register(self.getTemaById_async, 'expedientes.getTemaById')

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

