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

    def _getStatistics(self, initDate, endDate, userIds, officeIds, details):
        iDate = self._parseDate(initDate)
        eDate = self._parseDate(endDate)

        con = self.conn.get()
        try:
            logging.info('calculando estadisticas')
            statistics = self.assistanceModel.getStatistics(con, userIds, iDate, eDate, officeIds)
            logging.info(statistics)
            return statistics
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('assistance.get_statistics')
    @inlineCallbacks
    def getStatistics(self, initDate, endDate, userIds, officeIds, details):
        r = yield threads.deferToThread(self._getStatistics, initDate, endDate, userIds, officeIds, details)
        returnValue(r)

    def exortStatistics(self, initDate, endDate, userIds, officeIds, details):
        stats = self._getStatistics(initDate, endDate, userIds, officeIds, details)

        stat = stats[user.id][0]
        justifications = {}

        import uuid
        import pyoo
        calc = pyoo.Desktop('localhost', 2002)
        doc = calc.open_spreadsheet('templateUserStats.ods')
        try:
            sheet = doc.sheets[0]
            sheet[0,1].value = user.dni
            sheet[1,1].value = user.name
            sheet[2,1].value = user.lastname
            sheet[3,1].value = stat.position

            i = 5
            for ds in stat.dailyStats:
                sheet[i,2].value = ds.date if ds.date is not None else ''
                sheet[i,3].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(ds.start)) if ds.start is not None else ''
                sheet[i,4].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(ds.end)) if ds.end is not None else ''
                sheet[i,5].value = datetime.timedelta(seconds=ds.periodSeconds) if ds.start is not None else ''
                sheet[i,6].value = ds.iin if ds.iin is not None else ''
                sheet[i,7].value = ds.out if ds.out is not None else ''
                sheet[i,8].value = datetime.timedelta(seconds=ds.workedSeconds) if ds.iin is not None else ''
                #sheet[i,9].value = datetime.timedelta(seconds=ds.workedSeconds - ds.periodSeconds) if ds.start is not None or ds.iin is not None else ''
                sheet[i,10].value = datetime.timedelta(seconds=ds.lateSeconds) if ds.lateSeconds > 0 else ''
                sheet[i,11].value = datetime.timedelta(seconds=ds.earlySeconds) if ds.earlySeconds > 0 else ''
                sheet[i,12].value = ds.justification.identifier if ds.justification is not None else ''
                sheet[i,13].value = Status.getIdentifier(ds.justification.status) if ds.justification is not None else ''

                if ds.justification is not None and ds.justification.status == 2:
                    if ds.justification.identifier not in justifications:
                        justifications[ds.justification.identifier] = 1
                    else:
                        justifications[ds.justification.identifier] = justifications[ds.justification.identifier] + 1

                i = i + 1

            i = i + 2
            for j in justifications.keys():
                sheet[i,0].value = j
                sheet[i,1].value = justifications[j]
                i = i + 1

            fn = '{}/{}-{}-{}.xlsx'.format(rp, user.lastname, user.name, user.dni)
            logging.info('salvando : {}'.format(fn))
            doc.save(fn, pyoo.FILTER_EXCEL_2007)

        finally:
            doc.close()

    @autobahn.wamp.register('assistance.export_statistics')
    @inlineCallbacks
    def exportStatistics(self, initDate, endDate, userIds, officeIds, details):
        r = yield threads.deferToThread(self._exportStatistics, initDate, endDate, userIds, officeIds, details)
        returnValue(r)
