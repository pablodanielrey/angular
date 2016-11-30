# -*- coding: utf-8 -*-
from model.serializer import JSONSerializable
from model.dao import DAO
from model.users.users import UserDAO, User
import re
import uuid


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


class PositionDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS designations.positions (
                  id VARCHAR PRIMARY KEY,
                  position VARCHAR,
                  type INTEGER,
                  created TIMESTAMPTZ default now()
                );
            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, r):
        d = Position()
        d.id = r['id']
        d.position = r['position']
        d.type = r['type']
        return d


    @classmethod
    def findByIds(cls, con, ids):
        assert ids is not None

        if len(ids) <= 0:
            return []

        cur = con.cursor()
        try:
            cur.execute('select * from designations.positions where id in %s', (tuple(ids),))
            if cur.rowcount <= 0:
                return []

            return [PositionDAO._fromResult(o) for o in cur.fetchall()]

        finally:
            cur.close()


    """
        TODO: HACK HORRIBLE PARA MANTENER FUNCIONANOD CODIGO DE ASISTENCIA Y OTROS SISTEMAS QUE
        SUPONEN 1 SOLO CARGO ACTIVO, POR ESO LO BUSCAN USANDO Position.findByUserId() Y NO Designations
    """
    @classmethod
    def findByUserId(cls, con, userId):
        cur = con.cursor()
        try:
            cur.execute('select dp.* from designations.positions dp, designations.designations d where d.position_id = dp.id and d.user_id = %s order by dstart desc limit 1', (userId,))
            return [cls._fromResult(r) for r in cur]
        finally:
            cur.close()
