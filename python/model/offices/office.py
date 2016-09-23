# -*- coding: utf-8 -*-
from model.serializer import JSONSerializable


class Office(JSONSerializable):

    officeType = ['unit', 'office', 'physical-office', 'area']

    def __init__(self):
        self.id = None
        self.parent = None
        self.name = None
        self.telephone = None
        self.number = None
        self.type = officeType[1]
        self.email = None
        self.designations = []
        self.childs = []

    def persist(self, con):
        return OfficeDAO.persist(con)

    @classmethod
    def findAll(cls, con, type=None):
        return OfficeDAO.findAll(con, type)

    @classmethod
    def findByIds(cls, con, ids):
        return OfficeDAO.findByIds(con, ids)


class Designation(JSONSerializable):

    def __init__(self):
        self.officeId = None
        self.position = 'Cumple función'
        self.userId = None
        self.start = None
        self.end = None


    @classmethod
    def findByIds(cls, con, ids):
        return DesignationDAO.findByIds(con, ids)


    @classmethod
    def getDesignationByUser(cls, con, userId, history=False):
        return DesignationDAO.getDesignationByUser(con, userId)


    @classmethod
    def getDesignationByOffice(cls, con, officeId, history=False):
        return DesignationDAO.getDesignationByOffice(con, officeId)


    @classmethod
    def getDesignationByPosition(cls, con, position, history=False):
        return DesignationDAO.getDesignationByPosition(con, position)


    def persist(self, con):
        return DesignationDAO.persist(con, self)


class OfficeModel():

    @classmethod
    def getOfficesByUser(cls, con, userId, tree=False, types=None):
        idsD = Designation.getDesignationByUser(con, userId)
        desig = Designation.findByIds(con, idsD)
        oIds = [d.officeId for d in desig]
        if types is None:
            return oIds

        offices = Office.findByIds(con, oIds)
        return [office.id for office in offices if office.type in types]

    @classmethod
    def getUsers(cls, con, oId):
        idsD = Designation.getDesignationByOffice(con, oId)
        desig = Designation.findByIds(con, idsD)
        uIds = []
        for d in desig:
            if d.userId not in uids:
                uIds.append(d.userId)
        return uIds
