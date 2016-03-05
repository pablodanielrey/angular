# -*- coding: utf-8 -*-
import logging
from model.files.files import FileDAO

class User:
    def __init__(self):
        self.id = None
        self.acceptedConditions = True
        self.email = None
        self.created = None
        self.cv = None


class UserDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create table laboral_insertion.users (
                    id varchar primary key,
                    accepted_conditions boolean default true,
                    email varhcar not null references profile.mails (id),
                    cv varchar not null references files.files (id),
                    created timestamptz default now()
                )
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        u = User()
        u.id = r['id']
        u.acceptedConditions = r['accepted_conditions']
        u.email = r['email']
        u.cv = r['cv']
        u.created = r['created']
        return u

    @staticmethod
    def persist(con, u):

        logging.info(u)

        if u.cv is not None and not FileDAO.check(con, u.cv):
            raise Exception('no existe el cv en la base de datos')

        cur = con.cursor()
        try:
            if u.id is None:
                u.id = str(uuid.uuid4())
                ins = u.__dict__
                ins['acceptedConditions'] = True
                cur.execute('insert into laboral_insertion.users (id, accepted_conditions, email, cv) values '
                            '(%(id)s, %(acceptedConditions)s, %(email)s, %(cv)s)', ins)
            else:
                ins = u.__dict__
                ins['acceptedConditions'] = True
                cur.execute('update laboral_insertion.users set accepted_conditions = %(acceptedConditions)s, email = %(email)s, '
                            'cv = %(cv)s where id = %(id)s', ins)
        finally:
            cur.close()

    @staticmethod
    def findAll(con):
        cur = con.cursor()
        try:
            cur.execute('select id from laboral_insertion.users')
            ins = [ x['id'] for x in cur ]
            return ins

        finally:
            cur.close()

    @staticmethod
    def findById(con, id):
        cur = con.cursor()
        try:
            cur.execute('select * from laboral_insertion.users where id = %s', (id,))
            ins = [ UserDAO._fromResult(x) for x in cur ]
            return ins

        finally:
            cur.close()
