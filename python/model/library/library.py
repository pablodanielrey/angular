
import datetime
from model.dao import DAO


class LibraryDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
              CREATE SCHEMA IF NOT EXISTS library;

              CREATE TABLE IF NOT EXISTS library.access (
                id VARCHAR NOT NULL PRIMARY KEY,
                user_id VARCHAR NOT NULL  REFERENCES profile.users (id),
                username VARCHAR,
                type INTEGER,
                date TIMESTAMPTZ DEFAULT now()
              );
            """)
        finally:
            cur.close()


    @classmethod
    def _fromResult(cls, r):
        a = AccessRegistry()
        a.id = r['id']
        a.userId = r['user_id']
        a.date = r['date']
        a.username = r['username']
        a.type = r['type']
        return a

    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            cur.execute('select * from library.access order by date')
            return [ cls._fromResult(r) for r in cur ]

        finally:
            cur.close()

    @classmethod
    def persist(cls, con, e):
        cur = con.cursor()
        try:
            cur.execute('insert into library.access (id, user_id, date, username, type) values (%(id)s, %(userId)s, %(date)s, %(username)s, %(type)s)', e.__dict__)

        finally:
            cur.close()

    @classmethod
    def findLastAccess(cls, con, userId):
        cur = con.cursor()
        try:
            cur.execute('select * from library.access where user_id = %s order by date desc limit 1', (userId,))
            if cur.rowcount <= 0:
                return None
            else:
                return cls._fromResult(cur.fetchone())

        finally:
            cur.close()


class AccessRegistry(JSONSerializable):

    dao = LibraryDAO

    def __init__(self):
        self.id = None
        self.userId = None
        self.date = None
        self.username = None
        self.type = None

    def persist(self, con):
        return self.dao.persist(con, self)

    @classmethod
    def findAll(cls, con):
        return cls.findAll(con)

    @classmethod
    def findLastAccess(cls, con, userId):
        return cls.dao.findLastAccess(con, userId)

    @classmethod
    def create(cls, con, userId, username):
        la = cls.findLastAccess(con, userId)
        if not la:
            ar = cls()
            ar.id = str(uuid.uuid4())
            ar.userId = userId
            ar.username = username
            ar.date = datetime.datetime.now()
            ar.type = 0
            return ar

        else:
            la.id = str(uuid.uuid4())
            la.username = username
            ar.date = datetime.datetime.now()
            la.type = (la.type + 1) % 2
            return la
