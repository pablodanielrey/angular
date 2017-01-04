# -*- coding: utf-8 -*-
from model.serializer import JSONSerializable
from model.dao import DAO
from model.users.users import UserDAO, User
import re
import uuid


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
    def findByFields(cls, con, params):
        return DesignationDAO.findByFields(con, params)


    @classmethod
    def findByUsers(cls, con, userIds, history=False):
        return DesignationDAO.findByUsers(con, userIds, history)

    @classmethod
    def findByPlaces(cls, con, placeIds, history=False):
        return DesignationDAO.findByPlaces(con, placeIds, history)

    def expire(self, con):
        DesignationDAO.expireByIds(con, [self.id])

    @classmethod
    def findByIds(cls, con, ids):
        return DesignationDAO.findByIds(con, ids)

    @classmethod
    def findByOffice(cls, con, officeId, history=False):
        if history:
            cond = {"office_id":[officeId], "dout":"IS NOT NULL"}
        else:
            cond = {"office_id":[officeId]}

        return DesignationDAO.findByFields(con, cond, {"dstart":"asc"})

    """
    @classmethod
    def getDesignationByPosition(cls, con, position, history=False):
        return DesignationDAO.getDesignationByPosition(con, position, history)
    """

    def persist(self, con):
        return DesignationDAO.persist(con, self)



class DesignationDAO(DAO):
    _schema = "designations."
    _table = "designation"

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS designations.designation (
                    id VARCHAR PRIMARY KEY,
                    user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                    office_id VARCHAR REFERENCES offices.offices (id),
                    position_id VARCHAR REFERENCES designations.positions (id),
                    parent_id VARCHAR REFERENCES designations.designation (id),
                    original_id VARCHAR REFERENCES designations.designation (id),

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
        except Error:
          print("error")
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        d = Designation()
        d.id = r['id']
        d.start = r['dstart']
        d.end = r['dend']
        d.out = r["dout"]
        d.description = r["description"]
        d.resolution = r["resolution"]
        d.record = r["record"]
        d.replaceId = r["parent_id"]
        d.originalId = r["original_id"]
        d.officeId = r['office_id']
        d.positionId = r['position_id']
        d.userId = r['user_id']

        return d

    @classmethod
    def expireByIds(cls, con, ids):
        assert ids is not None
        assert isinstance(ids, list)
        cur = con.cursor()
        try:
            cur.execute('update designations.designation set dout = NOW() where id in %s', (tuple(ids),))
        finally:
            cur.close()




    @classmethod
    def findByUsers(cls, con, userIds, history=False):
        assert userIds is not None
        assert isinstance(userIds, list)
        cur = con.cursor()
        try:
            if history is None or not history:
                cur.execute('select id from designations.designation where user_id IN %s and dout is null order by dstart',(tuple(userIds),))
            else:
                cur.execute('select id from designations.designation where user_id IN %s order by dstart',(tuple(userIds),))
            return [d['id'] for d in cur]
        finally:
            cur.close()


    @classmethod
    def findByPlaces(cls, con, placeIds, history=False):
        assert placeIds is not None
        assert isinstance(placeIds, list)

        if len(placeIds) <= 0:
            return []
        cur = con.cursor()
        try:
            if history is None or not history:
                cur.execute('select id from designations.designation where office_id IN %s and dout is null order by dstart',(tuple(placeIds),))
            else:
                cur.execute('select id from designations.designation where office_id IN %s order by dstart',(tuple(placeIds),))
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
            cur.execute('select * from designations.designation where id in %s order by dstart asc', (tuple(ids),))
            if cur.rowcount <= 0:
                return []

            return [DesignationDAO._fromResult(d) for d in cur.fetchall()]

        finally:
            cur.close()







    @classmethod
    def persist(cls, con, desig):
        cur = con.cursor()
        try:
            if not hasattr(desig, 'id'):
                desig.id = str(uuid.uuid4())
            cur.execute("insert into designations.designation (id, office_id, user_id, position_id, dstart, dend) "
                        "values (%(id)s, %(officeId)s, %(userId)s, %(positionId)s, %(start)s, %(end)s)",
                        desig.__dict__)
            return desig.id
        finally:
            cur.close()
