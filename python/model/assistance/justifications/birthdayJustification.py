# -*- coding: utf-8 -*-

from model.dao import DAO
from model.assistance.justifications.justifications import SingleDateJustification
from model.assistance.justifications.status import Status
import uuid, datetime

class BirthdayJustificationDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;
                create table assistance.justification_birthday (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    owner_id varchar not null references profile.users (id),
                    date date not null default now(),
                    created timestamptz default now()
                );
            """.format(BirthdayJustificationDAO.TABLE_NAME))
        finally:
            cur.close()

    @staticmethod
    def _fromResult(con, r):
        c = BirthdayJustification(r['user_id', r['owner_id'], r['date'])
        c.id = r['id']
        c.setStatus(Status.getLastStatus(con, c.id))
        return c

    @staticmethod
    def persist(con, c):
        assert c is not None

        cur = con.cursor()
        try:
            if ((not hasattr(c, 'id')) or (c.id is None)):
                c.id = str(uuid.uuid4())

                r = c.__dict__
                cur.execute('insert into assistance.justification_birthday (id, user_id, owner_id, date) '
                            'values ( %(id)s, %(userId)s, %(ownerId)s, %(date)s)', r)
            else:
                r = c.__dict__
                cur.execute('update assistance.justification_birthday set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'date = %(date)s where id = %(id)s', r)
            return id

        finally:
            cur.close()

    @staticmethod
    def findById(con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_birthday where id in %s', (tuple(ids),))
            return [ BirthdayDAO._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

    @staticmethod
    def findByUserId(con, userIds, start, end):
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)

        if len(userIds) <= 0:
            return

        cur = con.cursor()
        try:
            sDate = None if start is None else start.date()
            eDate = datetime.date.today() if end is None else end.date()
            cur.execute('select * from assistance.birthday where user_id  in %s and date BETWEEN %s AND %s', (tupe(userIds), sDate, eDate))
            return [ BirthdayDAO._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

class BirthdayJustification(SingleDateJustification):

    dao = BirthdayJustificationDAO

    def __init__(self, userId, ownerId, date):
        super().__init__(date, userId, ownerId)

    def getIdentifier(self):
        return "Cumpleaños"
