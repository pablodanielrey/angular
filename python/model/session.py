# -*- coding: utf-8 -*-
import uuid
import datetime
import inject
import psycopg2
import json

from model.config import Config
from model.utils import DateTimeEncoder

"""
datos de la entidad:

{
    id:'id de la sesion',
    data:'datos variables de sesion'
}

"""

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


    def findSession(self,id):
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            self.removeExpired(con)
            cur = con.cursor()
            cur.execute('select id,data,expire from system.sessions where id = %s',(id,))
            s = cur.fetchone()
            if s:
                return self.convertToDict(s)
            else:
                raise SessionNotFound()

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



    def destroy(self, id):
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            self.removeExpired(con)
            cur = con.cursor()
            cur.execute('delete from system.sessions where id = %s',(id,))
            con.commit()

        finally:
            con.close()


    def getSession(self,id):
        s = self.findSession(id)
        return s['data']
