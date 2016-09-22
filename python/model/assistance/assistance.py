
import logging
import json
import datetime
from dateutil.tz import tzlocal
import importlib
from model.assistance.logs import LogDAO, Log
from model.assistance.schedules import ScheduleDAO, Schedule
from model.serializer.utils import JSONSerializable

from model.assistance.justifications import *
from model.assistance.justifications.justifications import Justification
from model.assistance.justifications.justifications import Status

from model.positions.positions import Position
from model.offices.offices import Office
from model.assistance.statistics import WpStatistics
from model.assistance.utils import Utils

class ScheduleObject(JSONSerializable):

    def __init__(self, schedule=None, date = None):
        self.start = None if schedule is None else schedule.getStartDate(date)
        self.end = None if schedule is None else schedule.getEndDate(date)

class ScheduleData(JSONSerializable):

    def __init__(self, date = None, schedules = [], uid = None):
        self.userId = uid
        self.date = date
        self.schedules = [ScheduleObject(sc, date) for sc in schedules]
        self.hours = sum([int(s.getScheduleSeconds() / 60 /60) for s in schedules])


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

    def __init__(self, userId = None, workedAssistanceData = [], offices = []):
        self.userId = userId
        self.workedAssistanceData = workedAssistanceData
        self.offices = offices


class WorkPeriod(JSONSerializable):
    logsTolerance = datetime.timedelta(hours=2)

    @classmethod
    def _create(cls, userId, date):
        wp = WorkPeriod()
        wp.userId = userId
        wp.date = date
        return wp

    def __init__(self):
        self.userId = None
        self.date = None
        self.schedule = None
        self.logs = []
        self.justifications = []

    def addJustification(self, j):
        self.justifications.append(j)

    def getJustifications(self):
        return self.justifications

    def getDate(self):
        return self.date

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
        llogs = len(self.logs)
        if llogs == 0:
            return None
        if llogs % 2 == 1:
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

        lastLog = self.getEndLog().log
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

        startLog = self.getStartLog().log
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
                self.schedule = s
                break

    def _loadLogs(self, logs):
        if self.schedule is None:
            self.logs = []
            return self.logs

        """ carga los logs que estén dentro de la tolerancia para esa fecha de acuerdo al horario """
        if not self.schedule.daily:
            sd = self.schedule.getStartDate(self.date) - WorkPeriod.logsTolerance
            se = self.schedule.getEndDate(self.date) + WorkPeriod.logsTolerance
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

    @classmethod
    def isAssistance(cls, con, userId, start, end):
        """
            Chequea si ese usuario es controlado por el sistema de asistencia dentro de ese rango de fechas
            En realidad eso quiere decir si tiene algun horario definido dentro de las fechas especificadas
        """
        return len(Schedule.findByUserId(con, [userId], start, end)) > 0


    def _getSchedules(self, con, userIds, start, end):
        ss = ScheduleDAO.findByUserId(con, userIds, start, end)
        schedules = AssistanceModel._classifyByUserId(ss)
        return schedules

    def _getLogs(self, con, userIds, start, end):
        ls = LogDAO.findByUserId(con, userIds, start, end)
        logs = AssistanceModel._classifyByUserId(ls)
        return logs

    def _getJustifications(self, con, userIds, start, end):
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.date)
        assert isinstance(end, datetime.date)

        js = Justification.getJustifications(con, userIds, start, end)
        justs = AssistanceModel._classifyByUserId(js)
        return justs

    def getJustifications(self, con, userId, start, end, isAll = False):
        '''
            obtiene todas las justificaciones entre las fechas dadas (inclusivas)
            si isAll es True:
                entonces obtiene todas las justificaciones de la gente que pertenece a las oficinas para las cuales
                la persona tiene el rol autoriza.
            si isAll es False:
                entonces obtiene todas las justificaciones del usuario indicado por userId.
        '''
        assert isinstance(start, datetime.date)
        assert isinstance(end, datetime.date)

        userIds = []
        if isAll:
            # tengo que obtener todos los usuarios de las oficina que autoriaza y buscar por esos usuarios
            offices = Office.getOfficesByUserRole(con, userId, False, 'autoriza')
            userIds = Office.getOfficesUsers(con, offices)
            while userId in userIds:
                userIds.remove(userId)
        else:
            userIds.append(userId)

        return [] if len(userIds) <= 0 else self._getJustifications(con, userIds, start, end)

    def _isModifyJustification(self, con, userId, just, status):
        oldStatus = just.getStatus().status
        if userId == just.userId and oldStatus == Status.PENDING and  status == Status.CANCELED:
            return True

        if userId == just.userId:
            return False

        offices = Office.getOfficesByUserRole(con, userId, False, 'autoriza')
        userIds = Office.getOfficesUsers(con, offices)
        for uid in userIds:
            if uid == just.userId:
                return True

        return False


    def changeStatus(self, con, just, status, userId):
        '''
            status = UNDEFINED, PENDING, APPROVED, REJECTED, CANCELED
        '''
        # obtengo la constante correspondiente al estado
        s = getattr(Status, status)
        # verifico si tiene permisos para modificar el estado de la justificacion
        if self._isModifyJustification(con, userId, just, s):
            return just.changeStatus(con, s, userId)

        raise Exception('No posee permisos suficientes')


    def calculateStatistics(self, wps):
        userId = wps[0].userId
        stats = WpStatistics(userId)
        for wp in wps:
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

        assert start.tzinfo is not None
        assert end.tzinfo is not None

        logging.info('buscando los schedules')
        schedules = self._getSchedules(con, userIds, start, end)

        logging.info('buscando los logs')
        logs = self._getLogs(con, userIds, start, end + datetime.timedelta(days=1))

        logging.info('buscando las justificaciones')
        justifications = self._getJustifications(con, userIds, start.date(), (end + datetime.timedelta(days=1)).date())

        """ genero los dias a trabajar """
        logging.info('generando los dias de trabajo')
        days = []
        d = Utils._cloneDate(start.date())
        oneDay = datetime.timedelta(hours=24)
        dend = end.date()
        while d <= dend:
            days.append(d)
            d = d + oneDay

        """ genero todos los WorkPeriods para todos los usuarios """
        logging.info('generando los periodos de trabjo')
        wpss = {}
        for uid in userIds:
            wpss[uid] = [ WorkPeriod._create(uid, Utils._cloneDate(d)) for d in days ]

        """ cargar los datos de la base """
        logging.info('cargando los datos de los periodos')
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
                stats.updateStatistics(con, wp)
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
            oids = Office.getOfficesByUser(con, uid)
            offices = Office.findById(con, oids)
            for s in sts:
                for ds in s.dailyStats:
                    w = WorkedAssistanceData(ds)
                    ws.append(w)
                aData.append(AssistanceData(uid, ws, offices))

        return aData

    def getScheduleDataInWeek(self, con, userId, date):
        schedules = Schedule.findByUserIdInWeek(con, userId, date)
        return [ScheduleData(key, schedules[key], userId) for key in schedules]

    def createSingleDateJustification(self,con, date, userId, ownerId, justClazz, justModule):
        module = importlib.import_module(justModule)
        clazz = getattr(module, justClazz)
        j = clazz.create(con, date, userId, ownerId)
        jid = j.persist(con)
        if userId != ownerId:
            j.changeStatus(con, Status.APPROVED, ownerId)
        return jid


    def createRangedTimeWithoutReturnJustification(self, con, start, userId, ownerId, justClazz, justModule):
        # obtengo el schedule correspondiente

        wps = self.getWorkPeriods(con, [userId], start, start)
        wpsList = wps[userId]
        if len(wpsList) <= 0:
            raise Exception('No tiene un horario para la fecha ingresada')

        # saco el end del schedule
        end = wpsList[0].getEndDate()

        end = Utils._localizeLocal(end) if Utils._isNaive(end) else end

        module = importlib.import_module(justModule)
        clazz = getattr(module, justClazz)
        j = clazz.create(con, start, end, userId, ownerId)
        jid = j.persist(con)
        if userId != ownerId:
            j.changeStatus(con, Status.APPROVED, ownerId)
        return jid


    def createRangedTimeWithReturnJustification(self, con, start, end, userId, ownerId, justClazz, justModule):
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)
        module = importlib.import_module(justModule)
        clazz = getattr(module, justClazz)
        j = clazz.create(con, start, end, userId, ownerId)
        jid = j.persist(con)
        if userId != ownerId:
            j.changeStatus(con, Status.APPROVED, ownerId)
        return jid


    def createRangedJustification(self, con, start, days, userId, ownerId, justClazz, justModule):
        assert isinstance(start, datetime.date)
        module = importlib.import_module(justModule)
        clazz = getattr(module, justClazz)

        j = clazz.create(con, start, days, userId, ownerId)
        jid = j.persist(con)
        if userId != ownerId:
            j.changeStatus(con, Status.APPROVED, ownerId)
        return jid


    def getJustificationData(self, con, userId, date, justClazz, justModule):

        # obtengo el schedule correspondiente
        wps = self.getWorkPeriods(con, [userId], date, date)
        wpsList = wps[userId]
        schedule = wpsList[0] if len(wpsList) >= 0 else None

        module = importlib.import_module(justModule)
        clazz = getattr(module, justClazz)
        return clazz.getData(con, userId, date, schedule)

    def createScheduleWeek(self, con, userId, uid, date, scheds):
        # verificar si el userId tiene permisos para crear los schedules para el usuario uid
        # por ahora no lo verifico
        date = date - datetime.timedelta(days=date.weekday())
        for sc in scheds:
            s = Schedule()
            s.userId = uid
            s.date = date
            s.weekday = sc['weekday']
            s.start = sc['start'] * 60
            s.end = sc['end'] * 60
            s.daily = True
            s.persist(con)

    def createScheduleSpecial(self, con, userId, uid, date, scheds):
        # verificar si el userId tiene permisos para crear los schedules para el usuario uid
        # por ahora no lo verifico
        for sc in scheds:
            s = Schedule()
            s.userId = uid
            s.date = date
            s.weekday = date.weekday()
            s.start = sc['start'] * 60
            s.end = sc['end'] * 60
            s.daily = False
            s.persist(con)
