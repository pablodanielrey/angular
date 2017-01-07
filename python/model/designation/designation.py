# -*- coding: utf-8 -*-
from model.serializer import JSONSerializable
from model.dao import DAO

class Designation(JSONSerializable):

    def __init__(self):
        self.id = None
        self.officeId = None
        self.positionId = '1'
        self.userId = None
        self.start = None
        self.end = None
        self.out = None
        self.parentId = None
        self.resolution = None
        self.record = None
        self.originalId = None

    @classmethod
    def prueba(self, con):
        con['dao'].prueba(con)

    @classmethod
    def findByUsers(cls, con, userIds, history=False):
        return con['dao'].findByUsers(con, userIds, history)

    @classmethod
    def findByPlaces(cls, con, placeIds, history=False):
        return con['dao'].findByPlaces(con, placeIds, history)

    def expire(self, con):
        con['dao'].expireByIds(con, [self.id])

    @classmethod
    def findByIds(cls, con, ids):
        return con['dao'].findByIds(con, ids)

    @classmethod
    def findByOffice(cls, con, officeId, history=False):
        return con['dao'].findByOffice(con, officeId, history);

    """
    @classmethod
    def getDesignationByPosition(cls, con, position, history=False):
        return DesignationDAO.getDesignationByPosition(con, position, history)
    """

    def persist(self, con):
        return DesignationDAO.persist(con, self)


class DesignationDAO(DAO):

    @classmethod
    def prueba(cls):
        raise NotImplementedError()

    @classmethod
    def expireByIds(cls, con, ids):
        raise NotImplementedError()

    @classmethod
    def findByUsers(cls, con, userIds, history=False):
        raise NotImplementedError()

    @classmethod
    def findByPlaces(cls, con, placeIds, history=False):
        raise NotImplementedError()

    @classmethod
    def findByIds(cls, con, ids):
        raise NotImplementedError()

    @classmethod
    def findByOffice(cls, con, officeId, history=False):
        raise NotImplementedError()

    @classmethod
    def persist(cls, con, desig):
        raise NotImplementedError()
