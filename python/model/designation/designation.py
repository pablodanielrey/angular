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



class Designation(JSONSerializable):

    def __init__(self):
        self.id = None
        self.officeId = None
        self.positionId = '1'
        self.userId = None
        self.start = None
        self.end = None

    """
    @classmethod
    def removeByIds(cls, con, ids):
        DesignationDAO.removeByIds(con, ids)

    def remove(self, con):
        DesignationDAO.removeByIds(con, [self.id])

    """

    @classmethod
    def findAllByUser(cls, con, userId, history=False):
        return DesignationDAO.getDesignationsByUser(con, userId, history)

    def expire(self, con):
        DesignationDAO.expireByIds(con, [self.id])

    @classmethod
    def findByIds(cls, con, ids):
        return DesignationDAO.findByIds(con, ids)

    @classmethod
    def findByOffice(cls, con, officeId, history=False):
        return DesignationDAO.getDesignationsByOffice(con, officeId, history)

    """
    @classmethod
    def getDesignationByPosition(cls, con, position, history=False):
        return DesignationDAO.getDesignationByPosition(con, position, history)
    """

    def persist(self, con):
        return DesignationDAO.persist(con, self)



class DesignationDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS designations.designations (
                    id VARCHAR PRIMARY KEY,
                    user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                    office_id VARCHAR REFERENCES offices.offices (id),
                    position_id VARCHAR REFERENCES designations.positions (id),
                    parent_id VARCHAR REFERENCES designations.designations (id),
                    original_id VARCHAR REFERENCES designations.designations (id),

                    dstart DATE default now(),
                    dend DATE,
                    dout DATE,
                    description VARCHAR NOT NULL,
                    resolution VARCHAR,
                    record VARCHAR,

                    old_id INTEGER NOT NULL,
                    old_type VARCHAR NOT NULL,
                    old_resolution_out VARCHAR,
                    old_record_out VARCHAR,

                    created timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        d = Designation()
        d.id = r['id']
        d.officeId = r['office_id']
        d.position_id = r['position_id']
        d.userId = r['user_id']
        d.start = r['dstart']
        d.end = r['dend']
        return d

    @classmethod
    def expireByIds(cls, con, ids):
        assert ids is not None
        assert isinstance(ids, list)
        cur = con.cursor()
        try:
            cur.execute('update designations.designations set dend = NOW() where id in %s', (tuple(ids),))
        finally:
            cur.close()


    """
    @classmethod
    def removeByIds(cls, con, ids):
        assert ids is not None
        assert isinstance(ids, list)
        cur = con.cursor()
        try:
            cur.execute('delete from offices.designation where id in %s', (ids,))

        finally:
            cur.close()

    """

    @classmethod
    def getDesignationsByUser(cls, con, userId, history=False):
        assert userId is not None
        cur = con.cursor()
        try:
            if history is None or not history:
                cur.execute('select id from designations.designations where user_id = %s and dout is null order by dstart',(userId,))
            else:
                cur.execute('select id from designations.designations where user_id = %s order by dstart',(userId,))
            return [d['id'] for d in cur]
        finally:
            cur.close()

    @classmethod
    def findByIds(cls, con, ids):
        assert ids is not None
        assert isinstance(ids, list)

        if len(ids) <= 0:
            return []

        cur = con.cursor()
        try:
            cur.execute('select * from designations.designations where id in %s order by dstart asc', (tuple(ids),))
            if cur.rowcount <= 0:
                return []

            return [DesignationDAO._fromResult(d) for d in cur.fetchall()]

        finally:
            cur.close()

    @classmethod
    def getDesignationsByOffice(cls, con, officeId, history=False):
        assert officeId is not None
        cur = con.cursor()
        try:
            if history is None or not history:
                cur.execute('select id from designations.designations where office_id = %s and dout is null order by dstart asc',(officeId,))
            else:
                cur.execute('select id from designations.designations where office_id = %s order by dstart asc',(officeId,))

            return [d['id'] for d in cur]

        finally:
            cur.close()

    """
    @classmethod
    def getDesignationsByPosition(cls, con, position, history=False):
        assert position is not None
        cur = con.cursor()
        try:
            if history is None or not history:
                cur.execute('select id from offices.designation where position = %s and dend is null',(position,))
            else:
                cur.execute('select id from offices.designation where position = %s',(position,))

            return [d['id'] for d in cur]

        finally:
            cur.close()
    """



    @classmethod
    def persist(cls, con, desig):
        cur = con.cursor()
        try:
            if not hasattr(desig, 'id'):
                desig.id = str(uuid.uuid4())
            cur.execute("insert into designations.designations (id, office_id, user_id, position_id, dstart, dend) "
                        "values (%(id)s, %(officeId)s, %(userId)s, %(positionId)s, %(start)s, %(end)s)",
                        desig.__dict__)
            return desig.id
        finally:
            cur.close()
