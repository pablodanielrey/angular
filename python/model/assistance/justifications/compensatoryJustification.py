# -*- coding: utf-8 -*-

from model.assistance.justifications.justifications import SingleDateJustification
from model.assistance.justifications.status import Status
import uuid, datetime

from model.dao import DAO
from model.users.users import UserDAO

class CompensatoryJustificationDAO(DAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        cls._createDependencies(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_compensatory (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    owner_id varchar not null references profile.users (id),
                    date date not null default now(),
                    created timestamptz default now()
              );
              """
            cur.execute(sql)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, con, r):
        date = datetime.datetime.combine(r['date'], datetime.time.min)
        c = CompensatoryJustification(r['user_id'], r['owner_id'], date)
        c.id = r['id']
        c.setStatus(Status.getLastStatus(con, c.id))
        return c

    @classmethod
    def persist(cls, con, c):
        assert c is not None

        cur = con.cursor()
        try:
            if ((not hasattr(c, 'id')) or (c.id is None)) or (len(c.findById(con, [c.id])) <=  0):

                if ((not hasattr(c, 'id')) or (c.id is None)):
                    c.id = str(uuid.uuid4())

                r = c.__dict__
                cur.execute('insert into assistance.justification_compensatory (id, user_id, owner_id, date) '
                            'values ( %(id)s, %(userId)s, %(ownerId)s, %(date)s)', r)
            else:
                r = c.__dict__
                cur.execute('update assistance.justification_compensatory set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'date = %(date)s where id = %(id)s', r)
            return c.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_compensatory where id in %s', (tuple(ids),))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

    @classmethod
    def findByUserId(cls, con, userIds, start, end):
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)

        if len(userIds) <= 0:
            return

        cur = con.cursor()
        try:
            sDate = None if start is None else start.date()
            eDate = datetime.date.today() if end is None else end.date()
            cur.execute('select * from assistance.justification_compensatory where user_id  in %s and date BETWEEN %s AND %s', (tupe(userIds), sDate, eDate))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

class CompensatoryJustification(SingleDateJustification):

    dao = CompensatoryJustificationDAO

    def __init__(self, userId, ownerId, date):
        super().__init__(date, userId, ownerId)

    def getIdentifier(self):
        return "Compensatorio"
