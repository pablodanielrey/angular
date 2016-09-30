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
    def getLogs(self, date, details):

        ########################
        # ver como lo corregimos para que lo maneje wamp al tema del date.
        # tambien el docker parece no setear el timezone.
        import pytz
        timezone = pytz.timezone('America/Argentina/Buenos_Aires')

        logging.info(date)
        from dateutil.parser import parse
        date = parse(date)
        logging.info(date)

        from model.assistance.utils import Utils
        date = Utils._localizeUtc(date).astimezone(timezone)
        logging.info(date)
        #########################

        con = self.conn.get()
        try:
            logs = Log.findByDate(con, date)
            return logs
        finally:
            self.conn.put(con)
