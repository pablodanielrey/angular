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

    def getRegisterOptions(self):
        return autobahn.wamp.RegisterOptions(details_arg='details')


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
