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

        yield from self.register(self.rowByIdDestino_async, 'expedientes.destino.rowById')
        yield from self.register(self.gridDataDestino_async, 'expedientes.destino.gridData')
        yield from self.register(self.numRowsDestino_async, 'expedientes.destino.numRows')  
        yield from self.register(self.rowByIdExpediente_async, 'expedientes.expediente.rowById')
        yield from self.register(self.gridDataExpediente_async, 'expedientes.expediente.gridData')
        yield from self.register(self.numRowsExpediente_async, 'expedientes.expediente.numRows')  
        yield from self.register(self.rowByIdLugar_async, 'expedientes.lugar.rowById')
        yield from self.register(self.gridDataLugar_async, 'expedientes.lugar.gridData')
        yield from self.register(self.numRowsLugar_async, 'expedientes.lugar.numRows')  
        yield from self.register(self.rowByIdNota_async, 'expedientes.nota.rowById')
        yield from self.register(self.gridDataNota_async, 'expedientes.nota.gridData')
        yield from self.register(self.numRowsNota_async, 'expedientes.nota.numRows')  
        yield from self.register(self.rowByIdParticipacion_async, 'expedientes.participacion.rowById')
        yield from self.register(self.gridDataParticipacion_async, 'expedientes.participacion.gridData')
        yield from self.register(self.numRowsParticipacion_async, 'expedientes.participacion.numRows')  
        yield from self.register(self.rowByIdPersona_async, 'expedientes.persona.rowById')
        yield from self.register(self.gridDataPersona_async, 'expedientes.persona.gridData')
        yield from self.register(self.numRowsPersona_async, 'expedientes.persona.numRows')  
        yield from self.register(self.rowByIdTema_async, 'expedientes.tema.rowById')
        yield from self.register(self.gridDataTema_async, 'expedientes.tema.gridData')
        yield from self.register(self.numRowsTema_async, 'expedientes.tema.numRows')  

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    @coroutine
    def rowByIdDestino_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.rowByIdDestino, id)
        return r

    def rowByIdDestino(self, id):
        con = self._getDatabase()
        try:
            r = self.destino.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def gridDataDestino_async(self, filterParams):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.gridDataDestino, filterParams)
        return r

    def gridDataDestino(self, filterParams):
        con = self._getDatabase()
        try:
            r = {'data': None, 'status': 200}
            r['data'] = self.destino.gridData(con, filterParams)
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
    def rowByIdExpediente_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.rowByIdExpediente, id)
        return r

    def rowByIdExpediente(self, id):
        con = self._getDatabase()
        try:
            r = self.expediente.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def gridDataExpediente_async(self, filterParams):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.gridDataExpediente, filterParams)
        return r

    def gridDataExpediente(self, filterParams):
        con = self._getDatabase()
        try:
            r = {'data': None, 'status': 200}
            r['data'] = self.expediente.gridData(con, filterParams)
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
    def rowByIdLugar_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.rowByIdLugar, id)
        return r

    def rowByIdLugar(self, id):
        con = self._getDatabase()
        try:
            r = self.lugar.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def gridDataLugar_async(self, filterParams):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.gridDataLugar, filterParams)
        return r

    def gridDataLugar(self, filterParams):
        con = self._getDatabase()
        try:
            r = {'data': None, 'status': 200}
            r['data'] = self.lugar.gridData(con, filterParams)
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
    def rowByIdNota_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.rowByIdNota, id)
        return r

    def rowByIdNota(self, id):
        con = self._getDatabase()
        try:
            r = self.nota.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def gridDataNota_async(self, filterParams):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.gridDataNota, filterParams)
        return r

    def gridDataNota(self, filterParams):
        con = self._getDatabase()
        try:
            r = {'data': None, 'status': 200}
            r['data'] = self.nota.gridData(con, filterParams)
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
    def rowByIdParticipacion_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.rowByIdParticipacion, id)
        return r

    def rowByIdParticipacion(self, id):
        con = self._getDatabase()
        try:
            r = self.participacion.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def gridDataParticipacion_async(self, filterParams):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.gridDataParticipacion, filterParams)
        return r

    def gridDataParticipacion(self, filterParams):
        con = self._getDatabase()
        try:
            r = {'data': None, 'status': 200}
            r['data'] = self.participacion.gridData(con, filterParams)
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
    def rowByIdPersona_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.rowByIdPersona, id)
        return r

    def rowByIdPersona(self, id):
        con = self._getDatabase()
        try:
            r = self.persona.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def gridDataPersona_async(self, filterParams):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.gridDataPersona, filterParams)
        return r

    def gridDataPersona(self, filterParams):
        con = self._getDatabase()
        try:
            r = {'data': None, 'status': 200}
            r['data'] = self.persona.gridData(con, filterParams)
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
    def rowByIdTema_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.rowByIdTema, id)
        return r

    def rowByIdTema(self, id):
        con = self._getDatabase()
        try:
            r = self.tema.rowById(con, id)
            return r

        finally:
            con.close()

    @coroutine
    def gridDataTema_async(self, filterParams):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.gridDataTema, filterParams)
        return r

    def gridDataTema(self, filterParams):
        con = self._getDatabase()
        try:
            r = {'data': None, 'status': 200}
            r['data'] = self.tema.gridData(con, filterParams)
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

