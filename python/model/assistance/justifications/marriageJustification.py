# -*- coding: utf-8 -*-
'''
    implementa la justificación por Matrimonio
    dentro del registry debe existir una sección :

    [marriageJustification]
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


class MarriageJustificationAbstractDAO(AssistanceDAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_marriage (
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
                cur.execute('insert into assistance.justification_marriage (id, user_id, owner_id, jstart, jend, type) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(type)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_marriage set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s, type = %(type)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            logging.info('ids: %s', tuple(ids))
            cur.execute('select * from assistance.justification_marriage where id in %s',(tuple(ids),))
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
            cur.execute('select * from assistance.justification_marriage where user_id in %s and '
                        '(jstart <= %s and jend >= %s) and type = %s', (tuple(userIds), eDate, sDate, t))

            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

class MarriageJustificationDAO(MarriageJustificationAbstractDAO):

    type = 'MarriageJustification'

    @classmethod
    def _fromResult(cls, con, r):
        j = MarriageJustification(r['user_id'], r['owner_id'], r['jstart'], 0)
        j.id = r['id']
        j.end = r['jend']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j


class ChildMarriageJustificationDAO(MarriageJustificationAbstractDAO):

    type = 'ChildMarriageJustification'

    @classmethod
    def _fromResult(con, r):
        j = ChildMarriageJustification(r['user_id'], r['owner_id'], r['jstart'], 0)
        j.id = r['id']
        j.end = r['jend']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j


"""
    ENTIDADES
"""

class MarriageJustification(RangedJustification):

    dao = MarriageJustificationDAO
    registry = inject.instance(Registry).getRegistry('marriageJustification')

    def __init__(self, userId, ownerId, start, days = 0):
        assert isinstance(start, datetime.date)
        super().__init__(start, days, userId, ownerId)

    def getIdentifier(self):
        return 'Matrimonio'

    def getIdentifier(self):
        return 'Maternidad'

    def setEnd(self, date):
        assert isinstance(date, datetime.date)
        self.end = date


class ChildMarriageJustification(RangedJustification):

    dao = ChildMarriageJustificationDAO
    registry = inject.instance(Registry).getRegistry('childMarriageJustification')

    def __init__(self, userId, ownerId, start, days = 0):
        assert isinstance(start, datetime.date)
        super().__init__(start, days, userId, ownerId)

    def getIdentifier(self):
        return 'Matrimonio del hijo'

    def setEnd(self, date):
        assert isinstance(date, datetime.date)
        self.end = date

    def setStart(self, date):
        assert isinstance(date, datetime.date)
        self.start = date
