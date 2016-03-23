
import json
import datetime
from model.assistance.schedules import ScheduleDAO, Schedule
from model.assistance.utils import Serializer, JSONSerializable

class ScheduleDataSource:

    def findSchedule(self, start, end):
        pass

class LogsDataSource:

    def findLogs(self, start, end):
        pass


class WorkPeriod(JSONSerializable):

    tolerance = datetime.timedelta(hours=2)

    def __init__(self, date=None):
        self.userId = None
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
        import logging
        for s in reversed(schedules):
            if s.isValid(self.date):
                self.schedule = s


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

    def getWorkPeriods(self, con, userIds, start, end):
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)

        schedules = self._getSchedules(con, userIds, start, end)

        """ genero los dias a trabajar """
        days = []
        d = AssistanceModel._cloneDate(start.date())
        oneDay = datetime.timedelta(hours=24)
        dend = end.date()
        while d <= dend:
            days.append(d)
            d = d + oneDay

        """ ahora genero todos los WorkPeriods para todos los usuarios """
        wpss = {}
        for uid in userIds:
            wpss[uid] = [ WorkPeriod(AssistanceModel._cloneDate(d)) for d in days ]

        """ se proceden a cargar los datos de la base """
        for uid, wps in wpss.items():
            scheds = schedules[uid]
            for wp in wps:
                wp._loadSchedule(scheds)

        return wps
