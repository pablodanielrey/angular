
import logging
import json
import datetime
from dateutil.tz import tzlocal
from model.assistance.logs import LogDAO, Log
from model.assistance.schedules import ScheduleDAO, Schedule
from model.serializer.utils import JSONSerializable

from model.assistance.justifications.justifications import Justification
from model.assistance.statistics import WpStatistics


class WorkPeriod(JSONSerializable):

    logsTolerance = datetime.timedelta(hours=2)

    def __init__(self, userId = None, date = None):
        self.userId = userId
        self.date = date
        self.schedule = None
        self.logs = []
        self.justifications = []

    def addJustification(self, j):
        self.justifications.append(j)

    def getStartDate(self):
        if self.schedule is None:
            return None
        return self.schedule.getStartDate(self.date)

    def getEndDate(self):
        if self.schedule is None:
            return None
        return self.schedule.getEndDate(self.date)

    def getStartLog(self):
        if len(self.logs) <= 0:
            return None
        return self.logs[0]

    def getEndLog(self):
        if len(self.logs) <= 0:
            return None
        return self.logs[-1]

    def getWorkedSeconds(self):
        total = 0
        workingLogs = [ self.logs[k:k+2] for k in range(0, len(self.logs), 2) ]
        for wl in workingLogs:
            if len(wl) >= 2:
                total = total + (wl[1].log - wl[0].log).total_seconds()
        return total

    def _loadSchedule(self, schedules):
        """ el último schedule válido para esa fecha es el que vale """
        for s in reversed(schedules):
            if s.userId == self.userId and s.isValid(self.date):
                logging.info('eligiendo el schedule : {} para la fecha {}'.format(self.date, s.__dict__))
                self.schedule = s
                break

    def _loadLogs(self, logs):
        if self.schedule is None:
            self.logs = []
            return self.logs

        """ carga los logs que estén dentro de la tolerancia para esa fecha de acuerdo al horario """
        if not self.schedule.daily:
            sd = (self.schedule.getStartDate(self.date) - WorkPeriod.logsTolerance).replace(tzinfo=tzlocal())
            se = (self.schedule.getEndDate(self.date) + WorkPeriod.logsTolerance).replace(tzinfo=tzlocal())
            self.logs = [ l for l in logs if l.between(sd, se) ]
        else:
            self.logs = [ l for l in logs if l.between(self._getStartOfDay(), self._getEndOfDay()) ]

    def _getStartOfDay(self):
        return datetime.datetime.combine(self.date, datetime.time(0)).replace(tzinfo=tzlocal())

    def _getEndOfDay(self):
        return self._getStartOfDay() + datetime.timedelta(days=1)


class AssistanceModel:

    @staticmethod
    def _classifyByUserId(data):
        result = {}
        for d in data:
            if d.userId not in result:
                result[d.userId] = []
            result[d.userId].append(d)
        return result

    @staticmethod
    def _cloneDate(date):
        return datetime.date.fromordinal(date.toordinal())


    def _getSchedules(self, con, userIds, start, end):
        ss = ScheduleDAO.findByUserId(con, userIds, start, end)
        schedules = AssistanceModel._classifyByUserId(ss)
        return schedules

    def _getLogs(self, con, userIds, start, end):
        ls = LogDAO.findByUserId(con, userIds, start, end)
        logs = AssistanceModel._classifyByUserId(ls)
        return logs

    def _getJustifications(self, con, userIds, start, end):
        js = Justification.getJustifications(con, userIds, start, end)
        justs = AssistanceModel._classifyByUserId(js)
        return justs


    def calculateStatistics(self, wps):
        userId = wps[0].userId
        stats = WpStatistics(userId)
        for wp in wps:
            logging.info('calculando {}'.format(wp.date))
            stats.updateStatistics(wp)
        return stats


    def getWorkPeriods(self, con, userIds, start, end):
        """
            Calcula los datos de los WorkinPeriods de las personas entre las fechas.
            variables importantes :
                schedules -- schedules de las personas
                logs -- logs de las personas
                days -- dias generados entre las 2 fechas para calcular
                wpss -- working periods
                justifications -- justificaciones de las personas entre las fechas.
        """
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)

        logging.info('buscando los schedules')
        timer = datetime.datetime.now()
        schedules = self._getSchedules(con, userIds, start, end)
        logging.info(datetime.datetime.now() - timer)

        logging.info('buscando los logs')
        timer = datetime.datetime.now()
        logs = self._getLogs(con, userIds, start, end + datetime.timedelta(days=1))
        logging.info(datetime.datetime.now() - timer)
        """
        for lk in logs.keys():
            for l in logs[lk]:
                logging.info(l.__dict__)
        """

        logging.info('buscando las justificaciones')
        timer = datetime.datetime.now()
        justifications = self._getJustifications(con, userIds, start, end + datetime.timedelta(days=1))
        logging.info(datetime.datetime.now() - timer)

        """ genero los dias a trabajar """
        logging.info('generando los dias de trabajo')
        timer = datetime.datetime.now()
        days = []
        d = AssistanceModel._cloneDate(start.date())
        oneDay = datetime.timedelta(hours=24)
        dend = end.date()
        while d <= dend:
            days.append(d)
            d = d + oneDay
        logging.info(datetime.datetime.now() - timer)

        """ genero todos los WorkPeriods para todos los usuarios """
        logging.info('generando los periodos de trabjo')
        timer = datetime.datetime.now()
        wpss = {}
        for uid in userIds:
            wpss[uid] = [ WorkPeriod(uid, AssistanceModel._cloneDate(d)) for d in days ]
        logging.info(datetime.datetime.now() - timer)

        """ cargar los datos de la base """
        logging.info('cargando los datos de los periodos')
        timer = datetime.datetime.now()
        for uid, wps in wpss.items():
            scheds = []
            if uid in schedules:
                scheds = schedules[uid]

            log = []
            if uid in logs:
                log = logs[uid]

            for wp in wps:
                wp._loadSchedule(scheds)
                wp._loadLogs(log)

            """ cargo los datos de las justificaciones en los WorkedPeriod """
            if uid in justifications:
                for js in justifications[uid]:
                    js._loadWorkedPeriods(wps)

        logging.info(datetime.datetime.now() - timer)

        return wpss
     
     
 

