# -*- coding: utf-8 -*-
import logging
from model.dao import DAO
from model.files.files import FileDAO
from model.users.users import MailDAO

class User:
    def __init__(self):
        self.id = None
        self.acceptedConditions = True
        self.emailId = None
        self.created = None
        self.cv = None
        self.priority = 0

    @classmethod
    def findById(cls, con, uid):
        return UserDAO.findById(con, uid)

class UserDAO(DAO):
    dependencies = [FileDAO, MailDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)

        cur = con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS laboral_insertion;

                create table IF NOT EXISTS laboral_insertion.users (
                    id varchar primary key,
                    accepted_conditions boolean default true,
                    email varchar not null references profile.mails (id),
                    cv varchar not null references files.files (id),
                    priority integer default 0,
                    created timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        u = User()
        u.id = r['id']
        u.acceptedConditions = r['accepted_conditions']
        u.emailId = r['email']
        u.cv = r['cv']
        u.created = r['created']
        u.priority = r['priority']
        return u

    @staticmethod
    def persist(con, u):

        if u.id is None:
            raise Exception('Usuario no existente')

        cur = con.cursor()
        try:
            cur.execute('select id from laboral_insertion.users where id = %s', (u.id,))
            if cur.rowcount <= 0:
                ins = u.__dict__
                ins['acceptedConditions'] = True
                ins['cv'] = ins['cv'] if 'cv' in ins else None
                ins['priority'] = ins['priority'] if 'priority' in ins else 0
                logging.info('persist laboralinsertion.userdao {} {}'.format(u.id, u.emailId))
                cur.execute('insert into laboral_insertion.users (id, accepted_conditions, email, cv, priority) values '
                            '(%(id)s, %(acceptedConditions)s, %(emailId)s, %(cv)s, %(priority)s)', ins)
            else:
                ins = u.__dict__
                ins['acceptedConditions'] = True
                ins['cv'] = ins['cv'] if 'cv' in ins else None
                ins['priority'] = ins['priority'] if 'priority' in ins else 0
                cur.execute('update laboral_insertion.users set accepted_conditions = %(acceptedConditions)s, email = %(emailId)s, '
                            'cv = %(cv)s, priority = %(priority)s where id = %(id)s', ins)
        finally:
            cur.close()

    @staticmethod
    def deleteMail(con, mailId):
        if mailId is None:
            return

        cur = con.cursor()
        try:
            cur.execute('update laboral_insertion.users set email = null where email = %s', (mailId,))
            return mailId
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
