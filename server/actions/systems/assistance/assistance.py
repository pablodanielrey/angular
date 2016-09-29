# -*- coding: utf-8 -*-
import inject
import json
import re
import logging
import psycopg2


from twisted.internet.defer import inlineCallbacks
import autobahn
import wamp

from model.assistance.logs import Log

class Assistance(wamp.SystemComponentSession):

    conn = wamp.getConnectionManager()

    def getRegisterOptions(self):
        return autobahn.wamp.RegisterOptions(details_arg='details')

    @autobahn.wamp.register('assistance.get_logs')
    def getLogs(self, date, details):
        con = self.conn.get()
        try:
            return Log.findByDate(con, date)
        finally:
            self.conn.put(con)
