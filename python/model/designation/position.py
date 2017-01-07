# -*- coding: utf-8 -*-
from model.serializer import JSONSerializable
from model.designation.dao.positionDAO import PositionDAO

class Position(JSONSerializable):

    SUPPORT = 0
    NONTEACHING = 1
    TEACHING = 2

    def __init__(self):
        self.id = '1'
        self.position = 'Cumple función'
        self.type = self.SUPPORT

    """
        TODO: HACK HORRIBLE PARA MANTENER FUNCIONANOD CODIGO DE ASISTENCIA Y OTROS SISTEMAS QUE
        SUPONEN 1 SOLO CARGO ACTIVO, POR ESO LO BUSCAN USANDO Position.findByUserId() Y NO Designations
    """
    @classmethod
    def findByUserId(cls, con, userId):
        return PositionDAO.findByUserId(con, userId)

    @classmethod
    def findByIds(cls, con, ids):
        return PositionDAO.findByIds(con, ids)
