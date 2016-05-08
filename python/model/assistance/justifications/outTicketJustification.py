# -*- coding: utf-8 -*-
import logging
import datetime
import dateutil
import uuid


from model.assistance.justifications.justifications import Justification, RangedJustification, RangedTimeJustification
from model.assistance.justifications.status import Status

from model.assistance.assistanceDao import AssistanceDAO
from model.users.users import UserDAO

class OutTicketJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
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
            if not hasattr(j, 'end'):
                j.end = None

            if ((not hasattr(j, 'id')) or (j.id is None)):
                j.id = str(uuid.uuid4())

            if len(j.findById(con, [j.id])) <=  0:
                j.type = j.__class__.__name__
                r = j.__dict__
                cur.execute('insert into assistance.justification_out_ticket (id, user_id, owner_id, jstart, jend, type) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(type)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_out_ticket set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s, type = %(type)s where id = %(id)s', r)
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
            t = cls.type
            cur.execute('select * from assistance.justification_out_ticket where user_id in %s and (jstart <= %s and jend >= %s) and type = %s', (tuple(userIds), end, start, t))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()


class OutTicketWithReturnJustificationDAO(OutTicketJustificationDAO):

    type = "OutTicketWithReturnJustification"

    @classmethod
    def _fromResult(cls, con, r):
        j = OutTicketWithReturnJustification()
        j.userId = r['user_id']
        j.ownerId = r['owner_id']
        j.start = r['jstart']
        j.end = r['jend']
        j.id = r['id']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j


class OutTicketWithoutReturnJustificationDAO(OutTicketJustificationDAO):

    type = "OutTicketWithoutReturnJustification"

    @classmethod
    def _fromResult(cls, con, r):

        j = OutTicketWithoutReturnJustification()
        j.userId = r['user_id']
        j.ownerId = r['owner_id']
        j.start = r['jstart']
        j.end = r['jend']
        j.id = r['id']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j



class OutTicketJustification(RangedTimeJustification):

    def __init__(self, start = None, end=None, userId = None, ownerId = None):
        super().__init__(start, end, userId, ownerId)
        self.typeName = 'Boleta de salida'
        self.classType = RangedTimeJustification.__name__

    def persist(self, con):
        if self.start > self.end:
            raise Exception('La hora de finalización es menor que el inicio')

        diff = (self.end - self.start).seconds
        limitSeconds = 3 * 60 * 60
        if diff > limitSeconds:
            raise Exception('El tiempo requerido supera el límite')

        super().persist(con)


class OutTicketWithReturnJustification(OutTicketJustification):

    dao = OutTicketWithReturnJustificationDAO
    identifier = "con retorno"

    def __init__(self, start = None, end=None, userId = None, ownerId = None):
        super().__init__(start, end, userId, ownerId)
        self.identifier = OutTicketWithReturnJustification.identifier

    def getIdentifier(self):
        return self.typeName + " " + self.identifier

    def changeEnd(self, con, end):
        self.end = end
        OutTicketWithReturnJustificationDAO.persist(con)

class OutTicketWithoutReturnJustification(OutTicketJustification):

    dao = OutTicketWithoutReturnJustificationDAO
    identifier = 'sin retorno'

    def __init__(self, start = None, end = None, userId = None, ownerId = None):
        super().__init__(start, end, userId, ownerId)
        self.identifier = OutTicketWithoutReturnJustification.identifier

    def getIdentifier(self):
        return self.typeName + " " + self.indentifier

    def _loadWorkedPeriods(self, wps):
        assert self.getStatus() is not None
        if self.getStatus().status != Status.APPROVED:
            return

        for wp in wps:
            if wp.date == self.start.date() and  wp.getEndDate() >= self.start:
                self.wps.append(wp)
                wp.addJustification(self)
