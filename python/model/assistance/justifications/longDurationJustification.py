# -*- coding: utf-8 -*-
'''
    implementa la justificación de larga duración
    dentro del registry debe existir una sección :

    [longDurationJustification]
    continuousDays = True

'''
from model.connection.connection import Connection
from model.registry import Registry
import inject

from model.assistance.justifications.justifications import Justification, RangedJustification
from model.assistance.justifications.status import Status
import datetime, uuid

from model.assistance.assistanceDao import AssistanceDAO
from model.users.users import UserDAO


class LongDurationJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_long_duration (
                  id varchar primary key,
                  user_id varchar not null references profile.users (id),
                  owner_id varchar not null references profile.users (id),
                  jstart date default now(),
                  jend date default now(),
                  number bigint,
                  created timestamptz default now()
              );
            """
            cur.execute(sql)
        finally:
            cur.close()


    @classmethod
    def _fromResult(cls, con, r):
        j = LongDurationJustification(r['user_id'], r['owner_id'], r['jstart'], 0, r['number'])
        j.id = r['id']
        j.end = r['jend']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j

    @classmethod
    def persist(cls, con, j):
        assert j is not None

        cur = con.cursor()
        try:
            if ((not hasattr(j, 'id')) or (j.id is None)):
                j.id = str(uuid.uuid4())

            if len(j.findById(con, [j.id])) <=  0:
                r = j.__dict__
                cur.execute('insert into assistance.justification_long_duration(id, user_id, owner_id, jstart, jend, number) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(number)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_long_duration set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s, number = %(number)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_long_duration where id in %s', (tuple(ids),))
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
            cur.execute('select * from assistance.justification_long_duration where user_id in %s and '
                        '(jstart <= %s and jend >= %s)', (tuple(userIds), eDate, sDate))

            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()


class LongDurationJustification(RangedJustification):

    dao = LongDurationJustificationDAO
    registry = inject.instance(Registry).getRegistry('longDurationJustification')
    identifier = 'Larga Duración'

    def __init__(self, userId = None, ownerId = None, start = None, days = 0, number = None):
        super().__init__(start, days, userId, ownerId)
        self.number = number
        self.identifier = LongDurationJustification.identifier
        self.classType = RangedJustification.__name__

    def getIdentifier(self):
        return self.identifier

    def setEnd(self, date):
        assert isinstance(date, datetime.date)
        self.end = date

    def setStart(self, date):
        assert isinstance(date, datetime.date)
        self.start = date
