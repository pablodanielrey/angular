# -*- coding: utf-8 -*-
from model.assistance.justifications.status import Status
from model.serializer.utils import JSONSerializable

class Justification(JSONSerializable):

    def __init__(self, start, end, userId, ownerId):
        self.id = None
        self.start = start
        self.end = end
        self.userId = userId
        self.ownerId = ownerId
        self.status = None
        self.statusId = None
        self.StatusConst = Status.UNDEFINED
        self.wps = []

    def getIdentifier(self):
        return ''

    def persist(self, con):
        """ por defecto no hace nada """
        return

    def changeStatus(self, con, status, userId):
        assert status is not None
        assert (self.status is not None or self.statusId is not None)

        if self.status == None:
            self.status = Status.findByIds(con, [self.statusId])
        else:
            self.statusId = self.status.id

        self.status.changeStatus(con, self, status, userId)

    def _getLastStatus(self, con):
        if self.status is None:
            self.status = Status.getLastStatus(con, self.id)
            self.statusId = self.status.id
            self.statusConst = self.status.status

        return self.status

    def _loadWorkedPeriods(self, wps):
        """ por defecto no hace nada """
        return

    @classmethod
    def getJustifications(cls, con, userIds, start, end):
        """
            obtiene todas las justificaciones para esos usuarios entre esas fechas.
            las fechas son datetime y son incluídos.
            retorna un mapa :
                justifications[useId] = [justification1, justification2, .... ]
        """
        assert isinstance(userIds, list)
        ret = []
        for j in cls.__subclasses__():
            ret.extend(j.findByUserId(con, userIds, start, end))

        return ret
