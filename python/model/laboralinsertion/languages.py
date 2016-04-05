# -*- coding: utf-8 -*-
import uuid

class Language:
    def __init__(self):
        self.id = None
        self.userId = None
        self.name = None
        self.level = None

class LanguageDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create table laboral_insertion.languages (
                    id varchar not null primary key,
                    user_id varchar not null references laboral_insertion.users (id),
                    name varchar not null,
                    level varchar not null
                )
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        l = Language()
        l.id = r["id"]
        l.userId = r["user_id"]
        l.name = r["name"]
        l.level = r["level"]
        return l

    @staticmethod
    def persist(con, language):
        cur = con.cursor()
        try:
            if language.id is None:
                language.id = str(uuid.uuid4())
                ins = language.__dict__
                cur.execute('insert into laboral_insertion.languages (id, user_id, name, level) values '
                            '(%(id)s, %(userId)s, %(name)s, %(level)s)', ins)
            else:
                ins = language.__dict__
                cur.execute('update laboral_insertion.languages set user_id = %(userId)s, name = %(name)s,'
                            'level = %(level)s where id = %(id)s', ins)

        finally:
            cur.close()

    @staticmethod
    def deleteByUser(con, userId):
        cur = con.cursor()
        try:
            cur.execute('delete from laboral_insertion.languages where user_id = %s', (userId,))
        finally:
            cur.close()

    @staticmethod
    def findAll(con):
        cur = con.cursor()
        try:
            cur.execute('select id from laboral_insertion.languages')
            ins = [ x['id'] for x in cur ]
            return ins

        finally:
            cur.close()

    @staticmethod
    def findById(con, id):
        cur = con.cursor()
        try:
            cur.execute('select * from laboral_insertion.languages where id = %s', (id,))
            if cur.rowcount <= 0:
                return None
            r = cur.fetchone()
            return LanguageDAO._fromResult(r)

        finally:
            cur.close()

    @staticmethod
    def findByUser(con, userId):
        cur = con.cursor()
        try:
            cur.execute('select id from laboral_insertion.languages where user_id = %s', (userId,))
            ins = [ x['id'] for x in cur ]
            return ins

        finally:
            cur.close()
