# -*- coding: utf-8 -*-
'''
    implementa la justificación por Duelo
    dentro del registry debe existir una sección :

    [mourningJustification]
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


class MourningJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_mourning (
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

                cur.execute('insert into assistance.justification_mourning (id, user_id, owner_id, jstart, jend, type) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(type)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_mourning set user_id = %(userId)s, owner_id = %(ownerId)s, '
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
            cur.execute('select * from assistance.justification_mourning where id in %s',(tuple(ids),))
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
            cur.execute('select * from assistance.justification_mourning where user_id in %s and '
                        '(jstart <= %s and jend >= %s) and type = %s', (tuple(userIds), eDate, sDate, t))

            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()


class MourningFirstGradeJustificationDAO(MourningJustificationDAO):

    type = 'MourningFirstGradeJustification'

    @classmethod
    def _fromResult(cls, con, r):
        j = MourningFirstGradeJustification(r['user_id'], r['owner_id'], r['jstart'], 0)
        j.id = r['id']
        j.end = r['jend']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j

class MourningSecondGradeJustificationDAO(MourningJustificationDAO):

    type = 'MourningSecondGradeJustification'

    @classmethod
    def _fromResult(cls, con, r):
        j = MourningSecondGradeJustification(r['user_id'], r['owner_id'], r['jstart'], 0)
        j.id = r['id']
        j.end = r['jend']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j

class MourningRelativeJustificationDAO(MourningJustificationDAO):

    type = 'MourningRelativeJustification'

    @classmethod
    def _fromResult(cls, con, r):
        j = MourningRelativeJustification(r['user_id'], r['owner_id'], r['jstart'], 0)
        j.id = r['id']
        j.end = r['jend']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j


class MourningJustification(RangedJustification):

    registry = inject.instance(Registry).getRegistry('mourningJustification')

    def __init__(self, userId = None, ownerId = None, start = None, days = 0):
        super().__init__(start, days, userId, ownerId)
        self.typeName = "Duelo"
        self.classType = RangedJustification.__name__

    def setEnd(self, date):
        assert isinstance(date, datetime.date)
        self.end = date

    def setStart(self, date):
        assert isinstance(date, datetime.date)
        self.start = date


class MourningFirstGradeJustification(MourningJustification):

    dao = MourningFirstGradeJustificationDAO
    identifier = 'Fallecimiento pariente primer grado'

    def __init__(self, userId = None, ownerId = None, start = None, days = 0):
        super().__init__(userId, ownerId, start, days)
        self.identifier = MourningFirstGradeJustification.identifier

    def getIdentifier(self):
        return self.typeName + " " + self.identifier


class MourningSecondGradeJustification(MourningJustification):

    dao = MourningSecondGradeJustificationDAO
    identifier = 'Fallecimiento pariente segundo grado'

    def __init__(self, userId = None, ownerId = None, start = None, days = 0):
        super().__init__(userId, ownerId, start, days)
        self.identifier = MourningSecondGradeJustification.identifier

    def getIdentifier(self):
        return self.typeName + " " + self.identifier


class MourningRelativeJustification(MourningJustification):

    dao = MourningRelativeJustificationDAO
    identifier = 'Fallecimiento pariente político'

    def __init__(self, userId = None, ownerId = None, start = None, days = 0):
        super().__init__(userId, ownerId, start, days)
        self.identifier = MourningRelativeJustification.identifier

    def getIdentifier(self):
        return self.typeName + " " + self.identifier