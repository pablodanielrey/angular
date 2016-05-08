# -*- coding: utf-8 -*-


from model.serializer.utils import JSONSerializable



from model.dao import DAO
from model.users.users import UserDAO

class LogDAO(DAO):

    dependencies = [ UserDAO ]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
              CREATE SCHEMA IF NOT EXISTS assistance;

              CREATE TABLE IF NOT EXISTS assistance.attlog (
                id VARCHAR NOT NULL PRIMARY KEY,
                device_id VARCHAR NOT NULL,
                user_id VARCHAR NOT NULL  REFERENCES profile.users (id),
                verifymode BIGINT NOT NULL,
                log TIMESTAMPTZ NOT NULL,
                created TIMESTAMPTZ DEFAULT now()
              );
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        l = Log()
        l.id = r['id']
        l.deviceId = r['device_id']
        l.userId = r['user_id']
        l.verifyMode = r['verifymode']
        l.log = r['log']
        l.created = r['created']
        return l

    @staticmethod
    def findByUserId(con, ids, start, end):
        assert isinstance(ids, list)
        cur = con.cursor()
        try:
            cur.execute('select * from assistance.attlog where user_id in %s and log >= %s and log <= %s', (tuple(ids), start, end))
            return [ LogDAO._fromResult(r) for r in cur ]

        finally:
            cur.close()

    @classmethod
    def persist(cls, con, log):
        assert con is not None
        assert log is not None
        cur = con.cursor()
        try:
            if not hasattr(log, 'id') or log.id is None:
                log.id = str(uuid.uuid4())
            cur.execute('insert into assistance.attlog (id, device_id, user_id, verifymode, log) '
                        'select %(id)s, %(deviceId)s, %(userId)s, %(verifyMode)s, %(log)s where '
                        'not exists (select 1 from assistance.attlog where id = %(id)s)', log.__dict__)

        finally:
            cur.close()


class Log(JSONSerializable):

    def __init__(self):
        self.id = None
        self.deviceId = None
        self.userId = None
        self.verifyMode = 0
        self.log = None
        self.created = None

    def between(self, start, end):
        return (self.log >= start and self.log <= end)

    def persist(self, con):
        LogDAO.persist(con, self)
