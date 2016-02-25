# -*- coding: utf-8 -*-
import uuid
import datetime
import inject
import json

from model.registry import Registry
from model.utils import DateTimeEncoder


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

class Session:
    def __init__(self):
        self.id = None
        self.userId = None
        self.username = None
        self.created = None
        self.expire = None
        sefl.data = None

class SessionDAO:

    registry = inject.attr(Registry)

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute('create schema if not exists systems')
            cur.execute("""
                create table systems.sessions (
                    id varchar primary key,
                    user_id varchar,
                    username varchar,
                    expire timsetampz default now(),
                    created timestampz default now(),
                    data varchar
                )
            """)
        finally:
            cur.close()

    @staticmethod
    def persist(con, sess):
        cur = con.cursor()
        try:
            if sess.id is None:
                sess.id = str(uuid.uuid4())
                r = sess.__dict__
                cur.execute('insert into systems.sessions (id, user_id, username, expire, created, data)'
                            'values (%(id)s, %(userId)s, %(username)s, %(expire)s, %(created)s, %(data)s)', r)
            else:
                r = sess.__dict__
                cur.execute('update systems.sessions set expire = %(expire)s, data = %(data)s where id = %(id)s', r)

        finally:
            cur.close()


    @staticmethod
    def touch(con, sid):
        cur = con.cursor()
        try:
            cur.execute('select expire from systems.sessions where id = %s', (sid))
            if cur.rowcount <= 0:
                raise SessionNotFound()

            now = datetime.datetime.now()
            if cur.fetchone()['expire'] <= now:
                raise SessionExpired()

            exp = now + datetime.timedelta(minutes=int(registry.get(SessionDAO,'expire')))
            cur.execute('update systems.sessions set expire = %s where id = %s', (exp, sid))

        finally:
            cur.close()




    expire = datetime.timedelta(hours=1)
    config = inject.attr(Config)


    def __str__(self):
        return ''

    def convertToDict(self,s):
        session = {
            'id':s[0],
            'data':self.jsonToSession(s[1]),
            'expire':s[2]
        }
        return session

    def sessionToJson(self,s):
        jmsg = json.dumps(s, cls=DateTimeEncoder)
        return jmsg

    def jsonToSession(self,j):
        s = json.loads(j)
        return s


    def _findSession(self,con,id):
        self.removeExpired(con)
        cur = con.cursor()
        cur.execute('select id,data,expire from system.sessions where id = %s',(id,))
        s = cur.fetchone()
        if s:
            return self.convertToDict(s)
        else:
            raise SessionNotFound()


    def findSession(self,id):
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            return self._findSession(con, id)

        finally:
            con.close()


    def removeExpired(self,con):
        cur = con.cursor()
        cur.execute('delete from system.sessions where expire < now()')


    def getSessions(self):
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            self.removeExpired(con)
            cur = con.cursor()
            cur.execute('select id,data,expire from system.sessions')
            ss = cur.fetchall()
            sessions = []
            if ss:
                for s in ss:
                    sessions.append(self.convertToDict(s))

            return sessions

        finally:
            con.close()



    def _create(self,con,data):
        self.removeExpired(con)
        id = str(uuid.uuid4());
        actual = datetime.datetime.now()
        expire = actual + self.expire
        session = (id,self.sessionToJson(data),expire)

        cur = con.cursor()
        cur.execute('insert into system.sessions (id,data,expire) values (%s,%s,%s)',session)

        return id


    def create(self,data):
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            id = self._create(con,data)
            con.commit()
            return id

        finally:
            con.close()



    """
        actualiza el tiempo de expiración
    """
    def touch(self,id):
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            cur = con.cursor()
            cur.execute('update system.sessions set expire = %s where id = %s',(datetime.datetime.now() + self.expire,id))
            self.removeExpired(con)
            con.commit()

        finally:
            con.close()

    def _destroy(self, con, id):
        cur = con.cursor()
        cur.execute('delete from system.sessions where id = %s', (id,))

    def destroy(self, id):
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            self.removeExpired(con)
            self._destroy(con, id)
            con.commit()

        finally:
            con.close()

    def _getSession(self, con, id):
        s = self._findSession(con, id)
        if s is None:
            return None
        return s['data']


    def getSession(self,id):
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            return self._getSession(con,id)

        finally:
            con.close()
