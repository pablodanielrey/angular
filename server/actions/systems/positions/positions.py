# -*- coding: utf-8 -*-
import inject
import logging

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.registry import Registry
from model.connection import connection

from model.positions.positions import Position

from model.serializer.utils import MySerializer, JSONSerializable


class PositionsWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        reg = inject.instance(Registry)
        self.conn = connection.Connection(reg.getRegistry('dcsys'))

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getPosition_async, 'positions.getPosition')
        # yield from self.register(self.updatePosition_async, 'positions.updatePosition')

    def getPosition(self, userIds):
        con = self.conn.get()
        try:
            positions = Position.findByUser(con, userIds)
            return positions
        finally:
            self.conn.put(con)

    @coroutine
    def getPosition_async(self, userIds):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getPosition, userIds)
        return r
