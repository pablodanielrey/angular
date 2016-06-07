# -*- coding: utf-8 -*-
import datetime
import logging

from model.assistance.justifications.status import Status
from model.serializer.utils import JSONSerializable

class Justification(JSONSerializable):

    def __init__(self, userId = None, ownerId = None):
        self.id = None
        self.userId = userId
        self.ownerId = ownerId
        self.status = Status(userId, datetime.datetime.now())
        self.notes = None
        self.wps = []

    def getIdentifier(self):
        raise Exception('abstract method')

    def persist(self, con):
        jid = self.dao.persist(con, self)
        status = self.getStatus()
        status._setJustificationId(jid)
        status.persist(con)
        return jid

    def setStatus(self, s):
        self.status = s

    def getStatus(self):
        return self.status

    def changeStatus(self, con, statusConst, userId):
        assert statusConst is not None
        assert self.getStatus() is not None
        assert self.getStatus().id is not None
        self.getStatus().changeStatus(con, self, statusConst, userId)

    def getJustifiedSeconds(self, wp=None):
        return Exception('abstract method')

    def _getLastStatus(self, con):
        if self.getStatus() is None:
            self._setStatus(Status.getLastStatus(con, self.id))
        return self.getStatus()

    @classmethod
    def _loadStatus(cls, con, justs):
        """ carga el ultimo estado a cada una de las justificaciones """
        if len(justs) <= 0:
            return
        jids = [ j.id for j in justs ]
        statuses = Status.findByJustificationIds(con, jids)
        for j in justs:
            sts = [ s for s in statuses if s.justificationId == j.id ]
            sts.sort(key=lambda x: x.date)
            lastStatus = sts[-1]
            j.setStatus(lastStatus)

    @classmethod
    def findByUserId(cls, con, userIds, start, end):
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.date)
        assert isinstance(end, datetime.date)
        assert cls.dao is not None

        if start == end:
            end = None if end is None else end + datetime.timedelta(days=1)
            
        justs = cls.dao.findByUserId(con, userIds, start, end)
        cls._loadStatus(con, justs)
        return justs

    @classmethod
    def findById(cls, con, ids):
        assert cls.dao is not None
        justs = cls.dao.findById(con, ids)
        cls._loadStatus(con, justs)
        return justs

    @classmethod
    def getJustifications(cls, con, userIds, start, end):
        """
            llama a los findByUserId de todas las sublcases hoja de la jerarquía
            las fechas son date y son inclusivas
            retorna un mapa :
                justifications[useId] = [justification1, justification2, .... ]
        """
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.date)
        assert isinstance(end, datetime.date)
        ret = []

        for j in cls._getLeafSubclasses():
            ret.extend(j.findByUserId(con, userIds, start, end))

        return ret

    @classmethod
    def _getLeafSubclasses(cls):
        finalSubC = []
        toProcess = cls.__subclasses__()
        if len(toProcess) <= 0:
            return []
        while len(toProcess) > 0:
            c = toProcess.pop()
            sc = c.__subclasses__()
            if len(sc) <= 0:
                finalSubC.append(c)
            else:
                toProcess.extend(sc)
        return finalSubC


    @classmethod
    def getData(cls, con, userId, date, schedule):
        data = {}
        data['sStart'] = None if schedule is None else schedule.getStartDate()
        data['sEnd'] = None if schedule is None else schedule.getEndDate()
        return data


class SingleDateJustification(Justification):

    def __init__(self, date = None, userId = None, ownerId = None):
        super().__init__(userId, ownerId)
        self.date = date

    def getDate(self):
        return self.date

    def _loadWorkedPeriods(self, wps):
        assert self.getStatus() is not None
        if self.getStatus().status != Status.APPROVED:
            return

        ### HORRIBLE HACK. charlarlo mañaan
        date = self.getDate()
        if isinstance(date, datetime.datetime):
            date = date.date()
        for wp in wps:
            if date == wp.getDate():
                self.wps.append(wp)
                wp.addJustification(self)

    def getJustifiedSeconds(self, wp=None):
        if wp.getSchedule() is None:
            return 0

        seconds = 0
        for wp in self.wps:
            if wp.getSchedule() is not None:
                seconds = seconds + (wp.getEndDate() - wp.getStartDate()).total_seconds()
        return seconds

    @classmethod
    def create(cls, con, date, userId, ownerId):
        return cls(date, userId, ownerId)


class RangedJustification(Justification):

    @staticmethod
    def _getEnd(start, days, continuous=False):
        if start is None and days > 0:
            return None
        '''
        le resto un dia al days porque el start es un dia a justificar
        '''
        days = days - 1

        if continuous:
            return start + datetime.timedelta(days=days)
        else:
            date = start
            while (days > 0):
                if date.weekday() >= 5:
                    date = date + datetime.timedelta(days = (7 - date.weekday()))
                else:
                    days = days - 1
                    date = date + datetime.timedelta(days=1)

            if date.weekday() >= 5:
                date = date + datetime.timedelta(days = (7 - date.weekday()))
            return date

    @classmethod
    def isContinuous(cls):
        if (cls.registry.get('continuousDays').lower() == 'true'):
            return True
        else:
            return False

    @classmethod
    def create(cls, con, start, days, userId, ownerId):
        return cls(start, days, userId, ownerId)


    def __init__(self, start = None, days = 0, userId = None, ownerId = None):
        super().__init__(userId, ownerId)

        continuous = self.isContinuous()
        self.start = start

        self.end = None if start is None or days is None else RangedJustification._getEnd(start, days, continuous)

    def _loadWorkedPeriods(self, wps):
        assert self.getStatus() is not None
        if self.getStatus().status != Status.APPROVED:
            return

        for wp in wps:
            if self.start <= wp.getDate() <= self.end:
                self.wps.append(wp)
                wp.addJustification(self)

    def getJustifiedSeconds(self, wp=None):
        """
            retorna la cantidad de segundos justificados.
            si se le pasa el día, entonces retorna los segundos del horario.
            si el wp es None entonces retorna la suma de todos los horarios de los días que justifica
        """
        if wp.getSchedule() is None:
            return 0

        seconds = 0
        if wp is None:
            for wp in self.wps:
                wstart = wp.getStartDate()
                wend = wp.getEndDate()
                if wstart is None or wend is None:
                    continue
                seconds = seconds + (wend - wstart).total_seconds()
            return seconds
        else:
            wstart = wp.getStartDate()
            wend = wp.getEndDate()
            if wstart is None or wend is None:
                return 0
            return (wend - wstart).total_seconds()


class RangedTimeJustification(Justification):

    def __init__(self, start = None, end = None, userId = None, ownerId = None):
        super().__init__(userId, ownerId)
        self.start = start
        self.end = end

    @classmethod
    def create(cls, con, start, end, userId, ownerId):
        return cls(start, end, userId, ownerId)

    def _loadWorkedPeriods(self, wps):
        assert self.getStatus() is not None
        if self.getStatus().status != Status.APPROVED:
            return

        from model.assistance.utils import Utils
        for wp in wps:
            wstart = Utils._localizeLocalIfNaive(wp.getStartDate())
            wend = Utils._localizeLocalIfNaive(wp.getEndDate())
            if wstart is not None and wend is not None and wstart <= self.end and wend >= self.start:
                self.wps.append(wp)
                wp.addJustification(self)

    def getJustifiedSeconds(self, wp=None):
        """
            retorna la cantidad de segundos justificados.
            Si end es None entonces retorna la cantidad de segundos desde el start hasta el fin del horario
            Si no tiene horario entonces retorna 0
        """
        if self.end is None:
            """
                justifica hasta el fin del horario
            """
            if wp.getSchedule() is None:
                return 0

            return (wp.getEndDate() - self.start).total_seconds()
        else:
            return (self.end - self.start).total_seconds()
