# -*- coding: utf-8 -*-
'''
    implementa la justificación de Pre exámen
    dentro del registry debe existir una sección :

    [preExamJustification]
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


class PreExamJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_pre_exam (
                  id varchar primary key,
                  user_id varchar not null references profile.users (id),
                  owner_id varchar not null references profile.users (id),
                  jstart date default now(),
                  jend date default now(),
                  type varchar not null,
                  created timestamptz default now()
              );
              """
            cur.execute(sql)
        finally:
            cur.close()


    @classmethod
    def persist(cls, con, j):
        assert j is not None

        cur = con.cursor()
        try:
            if ((not hasattr(j, 'id')) or (j.id is None)):
                j.id = str(uuid.uuid4())

            if len(j.findById(con, [j.id])) <=  0:
                j.type = j.__class__.__name__

                r = j.__dict__
                cur.execute('insert into assistance.justification_pre_exam (id, user_id, owner_id, jstart, jend, type) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(type)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_pre_exam set user_id = %(userId)s, owner_id = %(ownerId)s, '
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
            cur.execute('select * from assistance.justification_pre_exam where id in %s',(tuple(ids),))
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
            t = cls.type
            cur.execute('select * from assistance.justification_pre_exam where user_id in %s and '
                        '(jstart <= %s and jend >= %s) and t = %s', (tuple(userIds), eDate, sDate, t))

            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()


class SchoolPreExamJustificationDAO(PreExamJustificationDAO):
    type = 'SchoolPreExamJustification'

    @classmethod
    def _fromResult(cls, con, r):
        j = SchoolPreExamJustification(r['user_id'], r['owner_id'], r['jstart'], 0)
        j.id = r['id']
        j.end = r['jend']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j


class UniversityPreExamJustificationDAO(PreExamJustificationDAO):

    type = 'UniversityPreExamJustification'

    @classmethod
    def _fromResult(cls, con, r):
        j = UniversityPreExamJustification(r['user_id'], r['owner_id'], r['jstart'], 0)
        j.id = r['id']
        j.end = r['jend']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j


class PreExamJustification(RangedJustification):

    registry = inject.instance(Registry).getRegistry('preExamJustification')

    def __init__(self, userId, ownerId, start, days = 0):
        assert isinstance(start, datetime.date)
        super().__init__(start, days, userId, ownerId)

    def setEnd(self, date):
        assert isinstance(date, datetime.date)
        self.end = date

    def setStart(self, date):
        assert isinstance(date, datetime.date)
        self.start = date

class SchoolPreExamJustification(PreExamJustification):

    dao = SchoolPreExamJustificationDAO


    def __init__(self, userId, ownerId, start, days = 0):
        super().__init__(userId, ownerId, start, days)

    def getIdentifier(self):
        return 'Pre exámen Ensañanza Media'


class UniversityPreExamJustification(PreExamJustification):

    dao = UniversityPreExamJustificationDAO

    def __init__(self, userId, ownerId, start, days = 0):
        super().__init__(userId, ownerId, start, days)

    def getIdentifier(self):
        return 'Pre exámen Ensañanza Superior'
