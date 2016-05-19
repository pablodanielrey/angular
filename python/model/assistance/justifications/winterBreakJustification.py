# -*- coding: utf-8 -*-
'''
    implementa la justificación Vacacions de Invierno
    dentro del registry debe existir una sección :

    [winterBreakJustification]
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


class WinterBreakJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO, StatusDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_winter_break (
                  id varchar primary key,
                  user_id varchar not null references profile.users (id),
                  owner_id varchar not null references profile.users (id),
                  jstart date default now(),
                  jend date default now(),
                  notes varchar,
                  created timestamptz default now()
              );
              """
            cur.execute(sql)
        finally:
            cur.close()


    @classmethod
    def _fromResult(cls, con, r):
        j = WinterBreakJustification(r['user_id'], r['owner_id'], r['jstart'], 0)
        j.id = r['id']
        j.end = r['jend']
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
                cur.execute('insert into assistance.justification_winter_break (id, user_id, owner_id, jstart, jend, notes) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(notes)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_winter_break set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s, notes = %(notes)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            logging.info('ids: %s', tuple(ids))
            cur.execute('select * from assistance.justification_winter_break where id in %s',(tuple(ids),))
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
            cur.execute('select * from assistance.justification_winter_break where user_id in %s and '
                        '(jstart <= %s and jend >= %s)', (tuple(userIds), eDate, sDate))

            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()


class WinterBreakJustification(RangedJustification):

    dao = WinterBreakJustificationDAO
    registry = inject.instance(Registry).getRegistry('winterBreakJustification')
    identifier = 'Vacaciones de Invierno'

    def __init__(self, userId = None, ownerId = None, start = None, days = 0):
        super().__init__(start, days, userId, ownerId)
        self.identifier = WinterBreakJustification.identifier
        self.classType = RangedJustification.__name__

    def getIdentifier(self):
        return self.identifier
