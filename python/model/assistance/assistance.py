
import logging
import json
import datetime
from dateutil.tz import tzlocal
import pytz
import importlib
from model.assistance.logs import LogDAO, Log
from model.assistance.schedules import ScheduleDAO, Schedule, ScheduleHistory
from model.serializer import JSONSerializable

from model.assistance.justifications import *
from model.assistance.justifications.justifications import Justification
from model.assistance.justifications.justifications import Status

from model.designation.position import Position
from model.offices.office import Office
from model.offices.officeModel import OfficeModel

from model.assistance.statistics import WpStatistics, WorkedNote
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
            self._initialize(ds)


    def _initialize(self, ds):
        self.date = ds.date
        self.logStart = Utils._localizeLocal(ds.iin) if Utils._isNaive(ds.iin) else ds.iin
        self.logEnd = Utils._localizeLocal(ds.out) if Utils._isNaive(ds.out) else ds.out
        self.scheduleStart = Utils._localizeLocal(ds.start) if Utils._isNaive(ds.start) else ds.start
        self.scheduleEnd = Utils._localizeLocal(ds.end) if Utils._isNaive(ds.end) else ds.end


class StaticData(WorkedAssistanceData):

    def __init__(self, ds = None, position = None, notes = ''):
        super().__init__(ds)
        self.position = position
        self.notes = notes

    def _initialize(self, ds):
        super()._initialize(ds)
        self.userId = ds.userId
        self.workedSeconds = ds.workedSeconds
        self.justification = ds.justification
        self.startMode = ds.iMode
        self.endMode = ds.oMode
        self.notes = ''





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

    timezone = pytz.timezone('America/Argentina/Buenos_Aires')

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


    def getStatisticsData(self, con, userIds, start, end, officeIds=[], initTime=None, endTime=None):
        # si no se le pasa usuarios busca en el listado de oficinas
        if userIds is None or len(userIds) <= 0:
            userIds = OfficeModel.findOfficesUsers(con, officeIds)

        stats = self.getStatistics(con, userIds, start, end)
        aData = []
        for uid in userIds:
            sts = stats[uid]

            """ TODO: HACK HORRIBLE HASTA QUE SE DEFINA BIEN LO DE DESIGNACIONES """
            positions = Position.findByUserId(con, uid)
            position = positions[0].position if len(positions) > 0 else ''
            """ ------------- """

            for s in sts:
                aData.extend([self._createStaticData(con, ds, position) for ds in s.dailyStats if self._verifiedTime(ds, initTime, endTime)])
        return aData

    def _createStaticData(self, con, ds, position):
        noteObj = WorkedNote.find(con, ds.userId, ds.date)
        notes = '' if len(noteObj) <= 0 else noteObj[0].notes
        return StaticData(ds, position, notes)


    # verifico que los logos o el horario este entre los horarios pasados como parámetros
    def _verifiedTime(self, ds, initTime, endTime):
        if initTime == None or endTime == None:
            return True

        out = [None if ds.out is None else Utils._localizeUtc(ds.out).astimezone(self.timezone)][0]
        start = [None if ds.iin is None else Utils._localizeUtc(ds.iin).astimezone(self.timezone)][0]

        if not(out is None or start is None) and not(out.time() < initTime.time() or start.time() > endTime.time()):
            return True

        if not(ds.start is None or ds.end is None) and not(ds.end.time() < initTime.time() or ds.start.time() > endTime.time()):
            return True

    def setWorkedNote(self, con, userId, date, text):
        wn = WorkedNote()
        wn.userId = userId
        wn.date = date
        wn.notes = text
        return wn.persist(con)



    @classmethod
    def _utcToLocal(cls, date):
        return None if date is None else Utils._localizeUtc(date).astimezone(cls.timezone)

    '''
        guarda el horario semanal
        date: dia de vigencia
        schedules: [{date: date, weekday: 0-6, start: datetime, end: datetime}]
    '''
    @classmethod
    def persistScheduleWeek(cls, con, userId, date, schedules, description = 'Cambio de horario semanal'):
        # obtengo el horario semanal que ya posee
        scheds = Schedule.findByUserIdInWeek(con, userId, date, False)

        #  la eliminacion la tengo que sacar una vez que pueda eliminar desde la pantalla
        logging.info("schdules anteriores: {}".format(scheds))
        for d in scheds:
            [sc.delete(con) for sc in scheds[d] if sc.date == date]

        ids = []
        logging.info("schedules a agregar {}".format(schedules))
        for sc in schedules:
            s = Schedule()
            s.userId = userId
            s.date = date
            s.weekday = sc['weekday']

            sTime = None if sc["start"] is None else cls._utcToLocal(sc["start"]).time()
            s.start = [None if sTime is None else sTime.second + sTime.minute * 60 + sTime.hour * 60 * 60][0]

            if sc["end"] is None or s.start is None:
                s.end = None
                s.isNull = True
            else:
                eTime = None if sc["end"] is None else cls._utcToLocal(sc["end"]).time()
                eTime = eTime.second + eTime.minute * 60 + eTime.hour * 60 * 60
                s.end = eTime if s.start < eTime else eTime + 24 * 60 * 60

            s.daily = True
            s.special = False
            logging.info("presistiendo date:{} start:{} end:{}".format(s.date, s.start, s.end))
            ids.append(s.persist(con))

        sh = ScheduleHistory()
        sh.userId = userId
        sh.date = date
        sh.schedules = ids
        sh.description = description
        return sh.persist(con)

    '''
        guarda el horario semanal en formato de horas
        date: dia de vigencia
        schedules: [{date: date, weekday: 0-6, start: datetime, hours: int}]
    '''
    @classmethod
    def persistScheduleHours(cls, con, userId, date, schedules, description = 'Cambio de horario semanal por horas'):
        logging.info("schedules a agregar {}".format(schedules))
        ids = []
        for sc in schedules:
            s = Schedule()
            s.userId = userId
            s.date = date
            s.weekday = sc['weekday']

            sTime = None if sc["start"] is None else cls._utcToLocal(sc["start"]).time()
            s.start = [None if sTime is None else sTime.second + sTime.minute * 60 + sTime.hour * 60 * 60][0]

            if sc["hours"] is None or s.start is None or sc["hours"] <= 0:
                s.end = None
                s.isNull = True
            else:
                s.end = sc["hours"] * 60 * 60 + s.start

            s.daily = True
            s.special = False
            logging.info("presistiendo date:{} start:{} end:{}".format(s.date, s.start, s.end))
            ids.append(s.persist(con))

        sh = ScheduleHistory()
        sh.userId = userId
        sh.date = date
        sh.schedules = ids
        sh.description = description
        return sh.persist(con)


    '''
        guarda un horario especial
        schedules: [{start: datetime, end: datetime}]
    '''
    @classmethod
    def persistScheduleSpecial(cls, con, userId, schedules, description = 'Horario especial'):
        logging.info("schedules especiales a crear {}".format(schedules))
        ids = []
        date = None
        for sc in schedules:
            if sc['start'] is None or sc['end'] is None or sc['start'] >= sc['end']:
                continue

            startLocal = cls._utcToLocal(sc["start"])
            endLocal = cls._utcToLocal(sc["end"])

            s = Schedule()
            s.userId = userId
            s.date = startLocal.date()
            s.weekday = s.date.weekday()

            sTime = startLocal.time()
            s.start = sTime.second + sTime.minute * 60 + sTime.hour * 60 * 60

            s.end = (endLocal - startLocal).total_seconds() + s.start
            s.special = True
            s.daily = True

            if date is None:
                date = s.date

            logging.info("presistiendo date:{} start:{} end:{}".format(s.date, s.start, s.end))
            ids.append(s.persist(con))


        sh = ScheduleHistory()
        sh.userId = userId
        sh.date = date
        sh.schedules = ids
        sh.description = description
        return sh.persist(con)
