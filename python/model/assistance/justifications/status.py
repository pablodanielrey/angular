# -*- coding: utf-8 -*-
from model.serializer.utils import JSONSerializable
import datetime, logging
import uuid
from model.dao import DAO
from model.users.users import UserDAO

class Status(JSONSerializable):
    UNDEFINED = 0
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    CANCELED = 4

    def __init__(self, userId, date):
        self.id = None
        self.justificationId = None
        self.status = Status.PENDING
        self.userId = userId
        self.date = date
        self.created = datetime.datetime.now()

    def _setJustificationId(self, jid):
        self.justificationId = jid

    def persist(self, con):
        logging.info('persitiendo el estado : {}'.format(self.__dict__))
        assert self.justificationId is not None
        return StatusDAO.persist(con, self)

    def changeStatus(self, con, justification, statusConst, userId):
        assert userId is not None
        date = self.date + datetime.timedelta(seconds=1)
        s = Status(userId, date)
        s.justificationId = justification.id
        s.status = statusConst
        s.persist(con)
        justification.setStatus(s)

    @classmethod
    def findByJustificationIds(cls, con, ids):
        return StatusDAO.findByJustificationIds(con, ids)

    @classmethod
    def findByIds(cls, con, ids):
        return StatusDAO.findByIds(con, ids)

    @classmethod
    def getLastStatus(cls, con, jid):
        return StatusDAO.getLastStatus(con, jid)

class StatusDAO(DAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS assistance;
                
                CREATE TABLE IF NOT EXISTS assistance.justification_status (
                    id varchar primary key,
                    status int not null,
                    user_id varchar not null references profile.users (id),
                    justification_id varchar not null,
                    date timestamptz default now(),
                    created timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        s = Status(r['user_id'], r['date'])
        s.id = r['id']
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
            cur.execute('insert into assistance.justification_status (id, status, user_id, justification_id, date) '
                        'values (%(id)s, %(status)s, %(userId)s, %(justificationId)s, %(date)s)', r)
            return id
        finally:
            cur.close()

    @staticmethod
    def findByJustificationIds(con, ids):
        assert isinstance(ids, list)
        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_status where justification_id in %s', (tuple(ids),))
            return [ StatusDAO._fromResult(r) for r in cur ]
        finally:
            cur.close()


    @staticmethod
    def findByIds(con, ids):
        assert isinstance(ids, list)
        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_status where id in %s', (tuple(ids),))
            return [ StatusDAO._fromResult(r) for r in cur ]
        finally:
            cur.close()

    @staticmethod
    def getLastStatus(con, jid):
        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_status where justification_id = %s order by date desc limit 1', (jid,))
            if cur.rowcount <= 0:
                return None

            return StatusDAO._fromResult(cur.fetchone())
        finally:
            cur.close()
