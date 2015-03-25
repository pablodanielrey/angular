# -*- coding: utf-8 -*-
import json, base64, psycopg2, datetime, traceback, logging
import inject
import datetime
import itertools

from wexceptions import *

from model.profiles import AccessDenied
from model.utils import DateTimeEncoder
from model.config import Config

from model.systems.assistance.logs import Logs
from model.systems.assistance.date import Date

class Assistance:

    date = inject.attr(Date)
    logs = inject.attr(Logs)

    """ http://stackoverflow.com/questions/4998427/how-to-group-elements-in-python-by-n-elements """
    def _grouper(self, n, iterable, fillvalue=None):
        "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
        return itertools.zip_longest(*[iter(iterable)]*n, fillvalue=fillvalue)


    """ a partir de una lista de datetime obtiene los grupos de worked """
    def _getWorkedTimetable(self, dateList):
        worked = []
        bytwo = list(self._grouper(2,dateList))
        logging.debug(bytwo)
        for s,e in bytwo:
            w = { 'start':s, 'end':e, 'seconds':(e-s).total_seconds() if s is not None and e is not None and s <= e else 0 }
            worked.append(w)
        return worked


    """ controlo la tolerancia entre logs -- 5 minutos """
    def _checkTolerance(self, log):
        if self._dateBefore == None:
            self._dateBefore = log
            return True

        ret = (log - self._dateBefore) >  datetime.timedelta(minutes=5)
        self._dateBefore = log
        return ret


    """
        Obtiene el estado de asistencia del usuario
        IMPORANTE!!!
        la fecha se toma como aware y en zona local del cliente!!!
        se pasa a utc dentro de este método ya que se necesita saber el inicio del día y fin del día en zona local.
    """
    def getAssistanceStatus(self,con,userId,date=None):
        if date is None:
            date = self.date.now()

        """ el cero y el fin del día son de la zona local """
        From = date.replace(hour=0,minute=0,second=0,microsecond=0)
        To = date.replace(hour=23,minute=59,second=59,microsecond=0)

        From = self.date.awareToUtc(From)
        To = self.date.awareToUtc(To)

        logs = self.logs.findLogs(con,userId,From,To)

        logging.debug(logs)

        attlogs = list(map(lambda e : e['log'] , logs))

        self._dateBefore = None
        attlogs = list(filter(self._checkTolerance,attlogs))

        inside = 'Afuera' if len(attlogs) % 2 == 0 else 'Trabajando'
        worked = self._getWorkedTimetable(attlogs);


        sdate = None
        edate = None
        totalSeconds = 0

        if len(worked) > 0:
            sdate = worked[0]['start']
            edate = worked[-1]['end']
            totalSeconds = 0
            for w in worked:
                totalSeconds = totalSeconds + w['seconds']


        assistanceStatus = {
            'status': inside,
            'start': sdate,
            'end': edate,
            'logs': attlogs,
            'workedMinutes': totalSeconds / 60
        }
        return assistanceStatus
