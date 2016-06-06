# -*- coding: utf-8 -*-
'''
    implementa la justificación de maternidad
    dentro del registry debe existir una sección :

    [maternityJustification]
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
from model.assistance.justifications.status import StatusDAO

from model.assistance.assistanceDao import AssistanceDAO
from model.users.users import UserDAO

class MaternityJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO, StatusDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_maternity (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    owner_id varchar not null references profile.users (id),
                    jstart date default now(),
                    jend date default now(),
                    notes varchar,
                    number bigint,
                    created timestamptz default now()
              );
              """
            cur.execute(sql)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, con, r):
        j = MaternityJustification()
        j.id = r['id']
        j.userId = r['user_id']
        j.ownerId = r['owner_id']
        j.start = r['jstart']
        j.end = r['jend']
        j.number = r['number']
        j.notes = r['notes']
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
                cur.execute('insert into assistance.justification_maternity (id, user_id, owner_id, jstart, jend, number, notes) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(number)s, %(notes)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_maternity set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s, number = %(number)s, notes = %(notes)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            logging.info('ids: %s', tuple(ids))
            cur.execute('select * from assistance.justification_maternity where id in %s',(tuple(ids),))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

    @classmethod
    def findByUserId(cls, con, userIds, start, end):
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.date)
        assert isinstance(end, datetime.date)

        if len(userIds) <= 0:
            return

        cur = con.cursor()
        try:
            eDate = datetime.date.today() if end is None else end
            cur.execute('select * from assistance.justification_maternity where user_id in %s and '
                        '(jstart <= %s and jend >= %s)', (tuple(userIds), eDate, start))

            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()


class MaternityJustification(RangedJustification):

    dao = MaternityJustificationDAO
    registry = inject.instance(Registry).getRegistry('maternityJustification')
    identifier = 'Maternidad'

    def __init__(self, start = None, days = 0, userId = None, ownerId = None, number = None):
        super().__init__(start, days, userId, ownerId)
        self.number = number
        self.identifier = MaternityJustification.identifier
        self.classType = RangedJustification.__name__

    def getIdentifier(self):
        return self.identifier

    def setEnd(self, date):
        assert isinstance(date, datetime.date)
        self.end = date

    def setStart(self, date):
        assert isinstance(date, datetime.date)
        self.start = date
