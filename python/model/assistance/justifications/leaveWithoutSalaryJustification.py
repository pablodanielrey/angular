# -*- coding: utf-8 -*-
'''
    implementa la justificación de Licencia sin goce de sueldo
    dentro del registry debe existir una sección :

    [leaveWithoutSalaryJustification]
    continuousDays = True

'''

import inject
import logging
import json
import datetime
import uuid

from model.connection.connection import Connection
from model.registry import Registry

from model.assistance.justifications.justifications import Justification, RangedJustification
from model.assistance.justifications.status import Status

from model.assistance.assistanceDao import AssistanceDAO
from model.users.users import UserDAO


class LeaveWithoutSalaryJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_leave_without_salary (
                  id varchar primary key,
                  user_id varchar not null references profile.users (id),
                  owner_id varchar not null references profile.users (id),
                  jstart date default now(),
                  jend date default now(),
                  created timestamptz default now()
              );
              """
            cur.execute(sql)
        finally:
            cur.close()


    @classmethod
    def _fromResult(cls, con, r):
        j = LeaveWithoutSalaryJustification(r['user_id'], r['owner_id'], r['jstart'], 0)
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
                cur.execute('insert into assistance.justification_leave_without_salary (id, user_id, owner_id, jstart, jend) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_leave_without_salary set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            logging.info('ids: %s', tuple(ids))
            cur.execute('select * from assistance.justification_leave_without_salary where id in %s',(tuple(ids),))
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
            cur.execute('select * from assistance.justification_leave_without_salary where user_id in %s and '
                        '(jstart <= %s and jend >= %s)', (tuple(userIds), eDate, sDate))

            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()


class LeaveWithoutSalaryJustification(RangedJustification):

    dao = LeaveWithoutSalaryJustificationDAO
    registry = inject.instance(Registry).getRegistry('leaveWithoutSalaryJustification')
    identifier = 'Licencia sin goce de sueldo'

    def __init__(self, userId = None, ownerId = None, start = None, days = 0):
        super().__init__(start, days, userId, ownerId)
        self.identifier = LeaveWithoutSalaryJustification.identifier
        self.classType = RangedJustification.__name__

    def getIdentifier(self):
        return self.identifier

    def setEnd(self, date):
        assert isinstance(date, datetime.date)
        self.end = date

    def setStart(self, date):
        assert isinstance(date, datetime.date)
        self.start = date
