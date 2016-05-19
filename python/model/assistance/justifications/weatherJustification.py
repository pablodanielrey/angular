# -*- coding: utf-8 -*-

from model.assistance.assistanceDao import AssistanceDAO
from model.users.users import UserDAO

from model.assistance.justifications.justifications import SingleDateJustification
from model.assistance.justifications.status import Status
from model.assistance.justifications.status import StatusDAO
import uuid, datetime

class WeatherJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO, StatusDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_weather (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    owner_id varchar not null references profile.users (id),
                    date date not null default now(),
                    notes varchar,
                    created timestamptz default now()
              );
              """
            cur.execute(sql)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, con, r):
        date = datetime.datetime.combine(r['date'], datetime.time.min)
        c = WeatherJustification(date, r['user_id'], r['owner_id'])
        c.id = r['id']
        c.notes = r['notes']
        c.setStatus(Status.getLastStatus(con, c.id))
        return c

    @classmethod
    def persist(cls, con, c):
        assert c is not None

        cur = con.cursor()
        try:
            if ((not hasattr(c, 'id')) or (c.id is None)):
                c.id = str(uuid.uuid4())

            if len(c.findById(con, [c.id])) <=  0:
                r = c.__dict__
                cur.execute('insert into assistance.justification_weather (id, user_id, owner_id, date, notes) '
                            'values ( %(id)s, %(userId)s, %(ownerId)s, %(date)s, %(notes)s)', r)
            else:
                r = c.__dict__
                cur.execute('update assistance.justification_weather set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'date = %(date)s, notes = %(notes)s where id = %(id)s', r)
            return c.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_weather where id in %s', (tuple(ids),))
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
            cur.execute('select * from assistance.justification_weather where user_id  in %s and date BETWEEN %s AND %s', (tuple(userIds), sDate, eDate))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

class WeatherJustification(SingleDateJustification):

    dao = WeatherJustificationDAO
    identifier = "Incumbencias Climáticas"

    def __init__(self, date = None, userId = None, ownerId = None):
        super().__init__(date, userId, ownerId)
        self.identifier = WeatherJustification.identifier
        self.classType = SingleDateJustification.__name__

    def getIdentifier(self):
        return self.identifier
