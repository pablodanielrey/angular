
import logging
import json
import datetime
from dateutil.tz import tzlocal
from model.assistance.logs import LogDAO, Log
from model.assistance.schedules import ScheduleDAO, Schedule
from model.assistance.utils import Serializer, JSONSerializable


class WorkPeriod(JSONSerializable):

    logsTolerance = datetime.timedelta(hours=2)

    def __init__(self, userId = None, date = None):
        self.userId = userId
        self.date = date
        self.schedule = None
        self.logs = []

    def getStartDate(self):
        return self.schedule.getStartDate(self.date)

    def getEndDate(self):
        return self.schedule.getEndDate(self.date)

    def getStartLog(self):
        return self.logs[0]

    def getEndLog(self):
        return self.logs[-1]

    def _loadSchedule(self, schedules):
        """ el último schedule válido para esa fecha es el que vale """
        for s in reversed(schedules):
            if s.userId == self.userId and s.isValid(self.date):
                self.schedule = s
                break

    def _loadLogs(self, logs):
        if self.schedule is None:
            self.logs = []
            return self.logs

        """ carga los logs que estén dentro de la tolerancia para esa fecha de acuerdo al horario """
        sd = (self.schedule.getStartDate(self.date) - WorkPeriod.logsTolerance).replace(tzinfo=tzlocal())
        se = (self.schedule.getEndDate(self.date) + WorkPeriod.logsTolerance).replace(tzinfo=tzlocal())
        self.logs = [ l for l in logs if l.between(sd, se) ]


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
