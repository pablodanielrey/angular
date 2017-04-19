# -*- coding: utf-8 -*-
import inject
import logging
import uuid
# import asyncio
# from asyncio import coroutine
# from autobahn.asyncio.wamp import ApplicationSession

from model.tutoriascoordinadores.tutoriasCoordinadoresModel import TutoriasCoordinadoresModel


import autobahn
import wamp

class TutoriasCoordinadores(wamp.SystemComponentSession):

    @autobahn.wamp.register('tutorias.coordinadores.get_tutorias')
    def getTutorias(self, userId):
        #busqueda de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return TutoriasCoordinadoresModel.getTutorias(ctx, userId)

        finally:
            ctx.closeConn()



    @autobahn.wamp.register('tutorias.coordinadores.detail_tutoria')
    def detailTutoria(self, tutoriaId):
        #busqueda de usuario
        ctx = wamp.getContextManager()
        ctx.getConn()
        try:
            return TutoriasCoordinadoresModel.detailTutoria(ctx, tutoriaId)

        finally:
            ctx.closeConn()

