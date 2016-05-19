# -*- coding: utf-8 -*-
'''
    implementa el manejo de sesiones del sistema.
    dentro del registry debe existir una sección :

    [sessions]
    expire = 3600

'''
import uuid
import datetime
from dateutil import tz
import inject
import json

from model.connection.connection import Connection
from model.registry import Registry
from model.dao import DAO
#from model.utils import DateTimeEncoder


class SessionNotFound(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return 'Sesion no encontrada'

class SessionExpired(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return 'Sesion expirada'



class SessionDAO(DAO):

    registry = inject.instance(Registry).getRegistry('sessions')
    #registry = getRegistry()
    #registry = Reg()

    def _fromResult(self, r):
        s = Session()
        s.id = r['id']
        s.userId = r['user_id']
        s.username = r['username']
        s.created = r['created']
        s.expire = r['expire']
        s.deleted = r['deleted']
        s.data = r['data']
        return s

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists systems;

                create table IF NOT EXISTS systems.sessions (
                    id varchar primary key,
                    user_id varchar,
                    username varchar,
                    expire timestamptz default now(),
                    created timestamptz default now(),
                    deleted timestamptz,
                    data varchar
                );
            """)
        finally:
            cur.close()

    def persist(self, con, sess):
        cur = con.cursor()
        try:
            if sess.id is None:
                sess.id = str(uuid.uuid4())
                sess.created = datetime.datetime.now()
                sess.expire = sess.created + datetime.timedelta(minutes=int(self.registry.get('expire')))
                sess.deleted = None

                r = sess.__dict__
                cur.execute('insert into systems.sessions (id, user_id, username, expire, created, deleted, data)'
                            'values (%(id)s, %(userId)s, %(username)s, %(expire)s, %(created)s, %(deleted)s, %(data)s)', r)
            else:
                r = sess.__dict__
                cur.execute('update systems.sessions set expire = %(expire)s, deleted = %(deleted)s, data = %(data)s where id = %(id)s', r)

            return sess.id

        finally:
            cur.close()

    def touch(self, con, sid):
        cur = con.cursor()
        try:
            cur.execute('select expire from systems.sessions where id = %s', (sid,))
            if cur.rowcount <= 0:
                raise SessionNotFound()

            now = datetime.datetime.now(tz.tzlocal())
            if cur.fetchone()['expire'] <= now:
                raise SessionExpired()

            exp = now + datetime.timedelta(minutes=int(self.registry.get('expire')))
            cur.execute('update systems.sessions set expire = %s where id = %s', (exp, sid))

        finally:
            cur.close()

    def deleteById(self, con, ids = []):
        ''' elimina las sesiones identificadas por la lista de ids, retorna la cantidad de registros afectados '''
        if len(ids) <= 0:
            return 0

        cur = con.cursor()
        try:
            cur.execute('update systems.sessions set deleted = NOW() where id in %s', (tuple(ids)))
            return cur.rowcount

        finally:
            cur.close()


    def expire(self, con):
        ''' elimina las sesiones que ya han expirado '''
        cur = con.cursor()
        try:
            cur.execute('update systems.sessions set deleted = NOW() where expired <= NOW()')
            return cur.rowcount

        finally:
            cur.close()

    def findById(self, con, ids=[]):
        assert isinstance(ids, list)
        cur = con.cursor()
        try:
            cur.execute('select * from systems.sessions where id in %s and expire >= NOW()', (tuple(ids),))
            return [ self._fromResult(x) for x in cur ]

        finally:
            cur.close()

    """
    def sessionToJson(self,s):
        jmsg = json.dumps(s, cls=DateTimeEncoder)
        return jmsg
    """

    """
    def jsonToSession(self,j):
        s = json.loads(j)
        return s
    """


class Session:

    dao = SessionDAO

    def __init__(self):
        self.id = None
        self.userId = None
        self.username = None
        self.created = None
        self.expire = None
        self.deleted = None
        self.data = None

    """
    def _toJson(self):
        return json.dumps(self)

    @staticmethod
    def _fromJson(sess):
        s = Session()
        s.__dict__ = json.loads(sess)
        return s
    """

    def persist(self, con):
        self.dao.persist(con, self)

    @classmethod
    def deleteById(cls, con, sid):
        cls.dao.deleteById(con, sid)

    @classmethod
    def touch(cls, con, sid):
        return cls.dao.touch(con, sid)

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)
        return cls.dao.findById(con, ids)
