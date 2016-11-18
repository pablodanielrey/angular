# -*- coding: utf-8 -*-
import inject
import json
import re
import logging
import psycopg2

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import threads

import autobahn
import wamp

from model.sileg.sileg import SilegModel

class Sileg(wamp.SystemComponentSession):

    conn = wamp.getConnectionManager()
    """
    def getRegisterOptions(self):
        return autobahn.wamp.RegisterOptions(details_arg='details')
    """

    @autobahn.wamp.register('sileg.get_users')
    @inlineCallbacks
    def getUsers(self):
        r = yield threads.deferToThread(self._getUsers)
        returnValue(r)

    def _getUsers(self):
        try:
            con = self.conn.get()
            self.conn.readOnly(con)
            return SilegModel.getUsers(con)

        finally:
            self.conn.put(con)


    @autobahn.wamp.register('sileg.get_cathedras')
    @inlineCallbacks
    def getCathedras(self):
        r = yield threads.deferToThread(self._getCathedras)
        returnValue(r)

    def _getCathedras(self):
        try:
            con = self.conn.get()
            self.conn.readOnly(con)
            return SilegModel.getCathedras(con)

        finally:
            self.conn.put(con)


    @autobahn.wamp.register('sileg.find_positions_active_by_user')
    @inlineCallbacks
    def findPositionsActiveByUser(self, userId):
        r = yield threads.deferToThread(self._findPositionsActiveByUser, userId)
        returnValue(r)

    def _findPositionsActiveByUser(self, userId):
        try:
            con = self.conn.get()
            self.conn.readOnly(con)
            return SilegModel.findPositionsActiveByUser(con, userId)

        finally:
            self.conn.put(con)
