# -*- coding: utf-8 -*-
import logging
import datetime
import uuid


from model.assistance.justifications.justifications import Justification, RangedJustification, RangedTimeJustification
from model.assistance.justifications.status import Status
from model.assistance.justifications.status import StatusDAO

from model.assistance.assistanceDao import AssistanceDAO
from model.users.users import UserDAO

class TaskJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO, StatusDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
                CREATE SCHEMA IF NOT EXISTS assistance;

                create table IF NOT EXISTS assistance.justification_task (
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
                cur.execute('insert into assistance.justification_task (id, user_id, owner_id, jstart, jend, type) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(type)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_task set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s, type = %(type)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_task where id in %s', (tuple(ids),))
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
            cur.execute('''
                SELECT * from assistance.justification_task
                WHERE user_id in %s 
                AND (jstart <= %s AND jend >= %s) 
                AND type = %s
            ''', (tuple(userIds), end, start, t))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()


class TaskWithReturnJustificationDAO(TaskJustificationDAO):

    type = "TaskWithReturnJustification"

    @classmethod
    def _fromResult(cls, con, r):
        j = TaskWithReturnJustification()
        j.userId = r['user_id']
        j.ownerId = r['owner_id']
        j.start = r['jstart']
        j.end = r['jend']
        j.id = r['id']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j


class TaskWithoutReturnJustificationDAO(TaskJustificationDAO):

    type = "TaskWithoutReturnJustification"

    @classmethod
    def _fromResult(cls, con, r):
        j = TaskWithoutReturnJustification()
        j.userId = r['user_id']
        j.ownerId = r['owner_id']
        j.start = r['jstart']
        j.end = r['jend']
        j.id = r['id']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j

class TaskJustification(RangedTimeJustification):

    def __init__(self, start = None, end=None, userId = None, ownerId = None):
        super().__init__(start, end, userId, ownerId)
        self.typeName = "Boleta en comisión"
        self.classType = RangedTimeJustification.__name__


class TaskWithReturnJustification(TaskJustification):

    dao = TaskWithReturnJustificationDAO
    identifier = "con retorno"

    def __init__(self, start = None, end = None, userId = None, ownerId = None):
        super().__init__(start, end, userId, ownerId)
        self.identifier = TaskWithReturnJustification.identifier

    def getIdentifier(self):
        return self.typeName + " " + self.identifier

    def changeEnd(self, con, end):
        self.end = end
        TaskWithReturnJustificationDAO.persist(con)

class TaskWithoutReturnJustification(TaskJustification):

    dao = TaskWithoutReturnJustificationDAO
    identifier = "sin retorno"

    def __init__(self, start = None, end = None, userId = None, ownerId = None):
        super().__init__(start, end, userId, ownerId)
        self.identifier = TaskWithoutReturnJustification.identifier

    def getIdentifier(self):
        return self.typeName + " " + self.identifier

    def _loadWorkedPeriods(self, wps):
        assert self.getStatus() is not None
        if self.getStatus().status != Status.APPROVED:
            return

        for wp in wps:
            if wp.date == self.start.date() and  wp.getEndDate() >= self.start:
                self.wps.append(wp)
                wp.addJustification(self)
