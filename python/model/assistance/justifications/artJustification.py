# -*- coding: utf-8 -*-
'''
    implementa la justificación por ART
    dentro del registry debe existir una sección :

    [artJustification]
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

from model.dao import DAO
from model.users.users import UserDAO


class ARTJustificationDAO(DAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        cls._createDependencies(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_art (
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


    @staticmethod
    def _fromResult(con, r):
        j = ARTJustification(r['user_id'], r['owner_id'], r['jstart'], 0)
        j.id = r['id']
        j.end = r['jend']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j

    @staticmethod
    def persist(con, j):
        assert j is not None

        cur = con.cursor()
        try:
            if ((not hasattr(j, 'id')) or (j.id is None)):
                j.id = str(uuid.uuid4())

                r = j.__dict__
                cur.execute('insert into assistance.justification_art (id, user_id, owner_id, jstart, jend) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_art set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @staticmethod
    def findById(con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            logging.info('ids: %s', tuple(ids))
            cur.execute('select * from assistance.justification_art where id in %s',(tuple(ids),))
            return [ ARTJustificationDAO._fromResult(con, r) for r in cur ]
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
            cur.execute('select * from assistance.justification_art where user_id in %s and '
                        '(jstart <= %s and jend >= %s)', (tuple(userIds), eDate, sDate))

            return [ ARTJustificationDAO._fromResult(con, r) for r in cur ]
        finally:
            cur.close()


class ARTJustification(RangedJustification):

    dao = ARTJustificationDAO
    registry = inject.instance(Registry).getRegistry('artJustification')

    def __init__(self, userId, ownerId, start, days = 0):
        super().__init__(start, days, userId, ownerId)

    def getIdentifier(self):
        return 'ART'
