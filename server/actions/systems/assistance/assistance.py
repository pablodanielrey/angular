# -*- coding: utf-8 -*-
import inject
import json
import re
import logging
import psycopg2

from dateutil.parser import parse
import pytz

from twisted.internet.defer import inlineCallbacks
import autobahn
import wamp

from model.assistance.logs import Log
from model.assistance.utils import Utils
from model.assistance.assistance import AssistanceModel

logging.getLogger().setLevel(logging.INFO)

class Assistance(wamp.SystemComponentSession):

    assistanceModel = inject.attr(AssistanceModel)
    timezone = pytz.timezone('America/Argentina/Buenos_Aires')
    conn = wamp.getConnectionManager()

    def getRegisterOptions(self):
        return autobahn.wamp.RegisterOptions(details_arg='details')

    def _parseDate(self, strDate):
        ########################
        # ver como lo corregimos para que lo maneje wamp al tema del date.
        # tambien el docker parece no setear el timezone.
        date = parse(strDate)
        ldate = Utils._localizeUtc(date).astimezone(self.timezone)
        return ldate

    @autobahn.wamp.register('assistance.get_logs')
    def getLogs(self, initDate, endDate, initHours, endHours, details):
        iDate = self._parseDate(initDate)
        eDate = self._parseDate(endDate)
        iHours = self._parseDate(initHours)
        eHours = self._parseDate(endHours)

        con = self.conn.get()
        try:
            logs = Log.findByDateRange(con, iDate, eDate, iHours, eHours)
            return logs
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('assistance.get_statistics')
    def getStatistics(self, initDate, endDate, userIds, details):
        iDate = self._parseDate(initDate)
        eDate = self._parseDate(endDate)

        con = self.conn.get()
        try:
            logging.info('calculando estadisticas')
            statistics = self.assistanceModel.getStatistics(con, userIds, iDate, eDate)
            logging.info(statistics)
            return statistics
        finally:
            self.conn.put(con)
