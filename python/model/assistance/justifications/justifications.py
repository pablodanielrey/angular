# -*- coding: utf-8 -*-
import datetime
import logging

from model.assistance.justifications.status import Status
from model.serializer.utils import JSONSerializable

class Justification(JSONSerializable):

    def __init__(self, userId, ownerId):
        self.id = None
        self.userId = userId
        self.ownerId = ownerId
        self.status = Status(userId, datetime.datetime.now())
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
        assert cls.dao is not None
        justs = cls.dao.findByUserId(con, userIds, start, end)
        cls._loadStatus(con, justs)
        return justs


    @classmethod
    def findById(cls, con, ids):
        assert cls.dao is not None
        justs = cls.dao.findById(con, ids)
        cls._loadStatuses(con, justs)
        return justs

    @classmethod
    def getJustifications(cls, con, userIds, start, end):
        """
            llama a los findByUserId de todas las sublcases hoja de la jerarquía
            las fechas son datetime y son inclusivas
            retorna un mapa :
                justifications[useId] = [justification1, justification2, .... ]
        """
        assert isinstance(userIds, list)
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


class SingleDateJustification(Justification):

    def __init__(self, date, userId, ownerId):
        assert isinstance(date, datetime.datetime)
        super().__init__(userId, ownerId)
        self.date = date

    def getDate(self):
        return self.date

    def _loadWorkedPeriods(self, wps):
        assert self.getStatus() is not None
        if self.getStatus().status != Status.APPROVED:
            return

        date = self.getDate().date()
        for wp in wps:
            if date == wp.date:
                self.wps.append(wp)
                wp.addJustification(self)


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
        if (cls.registry.get('continuousDays').lower == 'true'):
            return True
        else:
            return False

    def __init__(self, start, days, userId, ownerId):
        super().__init__(userId, ownerId)
        continuous = self.isContinuous()
        self.start = start
        self.end = RangedJustification._getEnd(start, days, continuous)

    def _loadWorkedPeriods(self, wps):
        assert self.getStatus() is not None
        if self.getStatus().status != Status.APPROVED:
            return

        for wp in wps:
            if self.start <= wp.date <= self.end:
                self.wps.append(wp)
                wp.addJustification(self)

class RangedTimeJustification(Justification):

    def __init__(self, start, end, userId, ownerId):
        super().__init__(userId, ownerId)
        self.start = start
        self.end = end

    def _loadWorkedPeriods(self, wps):
        assert self.getStatus() is not None
        if self.getStatus().status != Status.APPROVED:
            return

        for wp in wps:
            if wp.getStartDate() <= self.end and  wp.getEndDate() >= self.start:
                self.wps.append(wp)
                wp.addJustification(self)
