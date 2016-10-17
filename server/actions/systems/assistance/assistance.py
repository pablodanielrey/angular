# -*- coding: utf-8 -*-
import inject
import json
import re
import logging
import psycopg2

from dateutil.parser import parse
import pytz

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import threads

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

    def _getLogs(self, initDate, endDate, initHours, endHours, details):
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

    @autobahn.wamp.register('assistance.get_logs')
    @inlineCallbacks
    def getLogs(self, initDate, endDate, initHours, endHours, details):
        r = yield threads.deferToThread(self._getLogs, initDate, endDate, initHours, endHours, details)
        returnValue(r)

    def _getStatistics(self, initDate, endDate, userIds, officeIds, initTime, endTime, details):
        iDate = self._parseDate(initDate)
        eDate = self._parseDate(endDate)
        iTime = self._parseDate(initTime)
        eTime = self._parseDate(endTime)

        con = self.conn.get()
        try:
            logging.info('calculando estadisticas')
            statistics = self.assistanceModel.getStatisticsData(con, userIds, iDate, eDate, officeIds, iTime, eTime)
            logging.info(statistics)
            return statistics
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('assistance.get_statistics')
    @inlineCallbacks
    def getStatistics(self, initDate, endDate, userIds, officeIds, initTime, endTime, details):
        r = yield threads.deferToThread(self._getStatistics, initDate, endDate, userIds, officeIds, initTime, endTime, details)
        returnValue(r)
