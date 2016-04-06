# -*- coding: utf-8 -*-
from model.serializer.utils import JSONSerializable
import datetime, logging
import uuid

class Status(JSONSerializable):
    UNDEFINED = 0
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    CANCELED = 4

    def __init__(self, jid, userId):
        self.id = None
        self.status = Status.PENDING
        self.justificationId = jid
        self.userId = userId
        self.created = datetime.datetime.now()

    def persist(self, con):
        return StatusDAO.persist(con,self)

    def changeStatus(self, con, justification, status, userId = None):

        if userId is None:
            userId = justification.userId

        s = Status(self.justificationId, userId)
        s.status = status
        s.id = StatusDAO.persist(con,s)

        justification.status = s
        justification.statusId = s.id
        justification.statusConst = s.status
        
    @classmethod
    def findByIds(cls, con, ids):
        return StatusDAO.findByIds(con, ids)

    @classmethod
    def getLastStatus(cls, con, jid):
        return StatusDAO.getLastStatus(con, jid)

class StatusDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;
                create table assistance.justification_status (
                    id varchar primary key,
                    status int,
                    user_id varchar not null references profile.users (id),
                    justification_id varchar,
                    created timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        s = Status(r['id'], r['user_id'])
        s.status = r['status']
        s.justificationId = r['justification_id']
        s.created = r['created']
        return s

    @staticmethod
    def persist(con, status):
        cur = con.cursor()
        try:
            id = str(uuid.uuid4())
            status.id = id
            r = status.__dict__
            cur.execute('insert into assistance.justification_status (id, status, user_id, justification_id, created) '
                        'values (%(id)s, %(status)s, %(userId)s, %(justificationId)s, %(created)s)', r)
            return id
        finally:
            cur.close()

    @staticmethod
    def findByIds(con, ids):
        assert isinstance(ids, list)
        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_status where id in %s', tuple(ids))
            return [ StatusDAO._fromResult(r) for r in cur ]
        finally:
            cur.close()

    @staticmethod
    def getLastStatus(con, jid):
        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_status where justification_id = %s order by created desc limit 1', (jid,))
            if cur.rowcount <= 0:
                return None

            return StatusDAO._fromResult(cur.fetchone())
        finally:
            cur.close()
