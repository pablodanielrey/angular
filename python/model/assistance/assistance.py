
import logging
import json
import datetime
from dateutil.tz import tzlocal
from model.assistance.logs import LogDAO, Log
from model.assistance.schedules import ScheduleDAO, Schedule
from model.serializer.utils import JSONSerializable

from model.assistance.justifications import *
from model.assistance.justifications.justifications import Justification

from model.positions.positions import Position
from model.assistance.statistics import WpStatistics
from model.assistance.utils import Utils


class WorkedAssistanceData(JSONSerializable):

    def __init__(self, ds = None):
        if (ds is None):
            self._initialize()
        else:
            self._initialize(ds.date, ds.iin, ds.out, ds.start, ds.end)


    def _initialize(self, date = None, logStart = None, logEnd = None, scheduleStart = None, scheduleEnd = None):
        self.date = date
        self.logStart = Utils._localizeLocal(logStart) if Utils._isNaive(logStart) else logStart
        self.logEnd = Utils._localizeLocal(logEnd) if Utils._isNaive(logEnd) else logEnd
        self.scheduleStart = Utils._localizeLocal(scheduleStart) if Utils._isNaive(scheduleStart) else scheduleStart
        self.scheduleEnd = Utils._localizeLocal(scheduleEnd) if Utils._isNaive(scheduleEnd) else scheduleEnd


class AssistanceData(JSONSerializable):

    def __init__(self, userId = None, workedAssistanceData = []):
        self.userId = userId
        self.workedAssistanceData = workedAssistanceData


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

    def getJustifications(self):
        return self.justifications

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
        """
            Retorna los segundos trabajados
        """
        total = 0
        workingLogs = [ self.logs[k:k+2] for k in range(0, len(self.logs), 2) ]
        for wl in workingLogs:
            if len(wl) >= 2:
                total = total + (wl[1].log - wl[0].log).total_seconds()
        return total

    def getSchedule(self):
        return self.schedule

    def getScheduleSeconds(self):
        """
            Retorna los segundos que debería trabajar
        """
        if self.schedule is None:
            return 0
        return self.schedule.getScheduleSeconds()

    def getEarlySeconds(self):
        """
            Retorna los segundos de salida temprana
            en el caso de no tener schedule entonces retorna 0
        """
        endDate = self.getEndDate()
        if self.schedule is None or endDate is None:
            return 0

        if self.getEndLog() is None:
            return 0

        lastLog = self.getEndLog().log.astimezone(tzlocal()).replace(tzinfo=None)
        return 0 if lastLog >= endDate else (endDate - lastLog).total_seconds()

    def getLateSeconds(self):
        """
            Retorna los segundos de tardanza
            en el caso de no tener schedule retorna 0
        """
        startDate = self.getStartDate()
        if self.schedule is None or startDate is None:
            return 0

        if self.getStartLog() is None:
            return 0

        startLog = self.getStartLog().log.astimezone(tzlocal()).replace(tzinfo=None)
        return 0 if startLog <= startDate else (startLog - startDate).total_seconds()

    def isAbsence(self):
        """
            Retorna true si representa una ausencia
        """
        return self.schedule is not None and len(self.logs) <= 0

    def isJustificatedAbsence(self):
        """
            Retorna true si representa una ausencia justificada
        """
        return self.isAbsence() and len(self.justifications) > 0

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

    def getJustifications(self, con, userId, start, end, isAll = False):
        if isAll:
            # tengo que obtener todos los usuarios de las oficina que autoriaza y buscar por esos usuarios
            # ahora hago la misma llamada pero despues lo tengo que cambiar cuando este terminado lo de office y los roles
            return self._getJustifications(con, [userId], start, end)
        else:
            return self._getJustifications(con, [userId], start, end)



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

    def getStatistics(self, con, userIds, start, end):
        wpss = self.getWorkPeriods(con, userIds, start, end)
        totalStats = []
        for uid in wpss.keys():
            stats = WpStatistics()
            stats.userId = uid
            pos = Position.findByUser(con, [uid])
            stats.position = pos[0].name if len(pos) > 0 else None
            for wp in wpss[uid]:
                stats.updateStatistics(wp)
            totalStats.append(stats)
        return self._classifyByUserId(totalStats)

    def getAssistanceData(self, con, userIds, start, end):
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)

        logging.info('assistanceData start:{} end {} userId:{}'.format(start, end, userIds[0]))
        stats = self.getStatistics(con, userIds, start, end)
        aData = []

        for uid in userIds:
            sts = stats[uid]
            ws = []
            for s in sts:
                for ds in s.dailyStats:
                    w = WorkedAssistanceData(ds)
                    ws.append(w)
                aData.append(AssistanceData(uid, ws))

        return aData
