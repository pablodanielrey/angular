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

logging.getLogger().setLevel(logging.INFO)

class Assistance(wamp.SystemComponentSession):

    conn = wamp.getConnectionManager()

    def getRegisterOptions(self):
        return autobahn.wamp.RegisterOptions(details_arg='details')

    @autobahn.wamp.register('assistance.get_logs')
    def getLogs(self, initDate, endDate, details):

        ########################
        # ver como lo corregimos para que lo maneje wamp al tema del date.
        # tambien el docker parece no setear el timezone.
        import pytz
        timezone = pytz.timezone('America/Argentina/Buenos_Aires')
        from dateutil.parser import parse
        initDate = parse(initDate)
        endDate = parse(endDate)

        from model.assistance.utils import Utils
        initDate = Utils._localizeUtc(initDate).astimezone(timezone)
        endDate = Utils._localizeUtc(endDate).astimezone(timezone)
        #########################

        con = self.conn.get()
        try:
            logs = Log.findByDateRange(con, initDate, endDate)
            return logs
        finally:
            self.conn.put(con)
