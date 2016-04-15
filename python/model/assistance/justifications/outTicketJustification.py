# -*- coding: utf-8 -*-
import logging
import datetime
import uuid


from model.assistance.justifications.justifications import Justification, RangedJustification
from model.assistance.justifications.status import Status

from model.dao import DAO
from model.users.users import UserDAO

class OutTicketJustificationDAO(DAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        cls._createDependencies(con)
        cur = con.cursor()
        try:
            sql = """
                CREATE SCHEMA IF NOT EXISTS assistance;
                create table IF NOT EXISTS assistance.justification_out_ticket (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    owner_id varchar not null references profile.users (id),
                    jstart timestamptz default now(),
                    jend timestamptz default now(),
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
            if not hasattr(j, 'end'):
                j.end = None

            if ((not hasattr(j, 'id')) or (j.id is None)):
                j.id = str(uuid.uuid4())

                r = j.__dict__
                cur.execute('insert into assistance.justification_out_ticket (id, user_id, owner_id, jstart, jend) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_out_ticket set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_out_ticket where id in %s', (tuple(ids),))
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
            cur.execute('select * from assistance.justification_out_ticket where jend != null and user_id in %s and (jstart <= %s and jend >= %s)', (tuple(userIds), end, start))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()


class OutTicketWithReturnJustificationDAO(OutTicketJustificationDAO):

    @classmethod
    def _fromResult(cls, con, r):
        j = OutTicketWithReturnJustification(r['user_id'], r['owner_id'], r['jstart'], r['jend'])
        j.id = r['id']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j


class OutTicketWithoutReturnJustificationDAO(OutTicketJustificationDAO):

    @classmethod
    def _fromResult(cls, con, r):
        j = OutTicketWithoutReturnJustification(r['user_id'], r['owner_id'], r['jstart'])
        j.id = r['id']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j

    @classmethod
    def findByUserId(cls, con, userIds, start, end):
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)

        if len(userIds) <= 0:
            return

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_out_ticket where user_id in %s and '
                        '(jstart <= %s and DATE(jstart) = %s) and jend = null', (tuple(userIds), end, start.date()))

            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

class OutTicketJustification(RangedTimeJustification):

    def __init__(self, userId, ownerId, start, end=None):
        super().__init__(start, end, userId, ownerId)


class OutTicketWithReturnJustification(OutTicketJustification):

    dao = OutTicketWithReturnJustificationDAO

    def __init__(self, userId, ownerId, start, end):
        super().__init__(userId, ownerId, start, end)

    def getIdentifier(self):
        return "Boleta de salida con retorno"

    def changeEnd(self, con, end):
        self.end = end
        OutTicketWithReturnJustificationDAO.persist(con)

class OutTicketWithoutReturnJustification(OutTicketJustification):

    dao = OutTicketWithoutReturnJustificationDAO

    def __init__(self, userId, ownerId, start):
        super().__init__(userId, ownerId, start)
        self.end = None

    def getIdentifier(self):
        return 'Boleta de salida sin retorno'

    def _loadWorkedPeriods(self, wps):
        assert self.getStatus() is not None
        if self.getStatus().status != Status.APPROVED:
            return

        for wp in wps:
            if wp.date == self.start.date() and  wp.getEndDate() >= self.start:
                self.wps.append(wp)
                wp.addJustification(self)
