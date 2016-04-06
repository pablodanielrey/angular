
import logging
import json
import datetime
from dateutil.tz import tzlocal
from model.assistance.logs import LogDAO, Log
from model.assistance.schedules import ScheduleDAO, Schedule
from model.serializer.utils import JSONSerializable


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
        last = None
        for l in self.logs:
            if last is None:
                last = l.log
            else:
                total = total + (l.log - last).total_seconds()
                last = None

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


    def getWorkPeriods(self, con, userIds, start, end):
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)

        logging.info('buscando los schedules')
        timer = datetime.datetime.now()
        schedules = self._getSchedules(con, userIds, start, end)
        logging.info(datetime.datetime.now() - timer)

        logging.info('buscando los logs')
        timer = datetime.datetime.now()
        logs = self._getLogs(con, userIds, start, end + datetime.timedelta(1))
        logging.info(datetime.datetime.now() - timer)
        for lk in logs.keys():
            for l in logs[lk]:
                logging.info(l.__dict__)

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

        """ ahora genero todos los WorkPeriods para todos los usuarios """
        logging.info('generando los periodos de trabjo')
        timer = datetime.datetime.now()
        wpss = {}
        for uid in userIds:
            wpss[uid] = [ WorkPeriod(uid, AssistanceModel._cloneDate(d)) for d in days ]
        logging.info(datetime.datetime.now() - timer)

        """ se proceden a cargar los datos de la base """
        logging.info('cargando los datos de los periodos')
        timer = datetime.datetime.now()
        for uid, wps in wpss.items():
            if uid in schedules:
                scheds = schedules[uid]
                log = logs[uid]
                for wp in wps:
                    wp._loadSchedule(scheds)
                    wp._loadLogs(log)
        logging.info(datetime.datetime.now() - timer)

        return wpss
