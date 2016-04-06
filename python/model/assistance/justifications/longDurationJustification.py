# -*- coding: utf-8 -*-
'''
    implementa la justificación de larga duración
    dentro del registry debe existir una sección :

    [longDurationJustification]
    continuousDays = True

'''
from model.connection.connection import Connection
from model.registry import Registry
from model.serializer.utils import JSONSerializable
import inject

from model.assistance.justifications.justifications import Justification
from model.assistance.justifications.status import Status
import datetime, uuid

class LongDurationJustification(JSONSerializable, Justification):

    def __init__(self, userId, ownerId, start, days = 0, number = None):
        self.id = None
        self.userId = userId
        self.ownerId = ownerId
        self.start = start
        self.number = number
        self.status = None
        self.statusId = None
        self.StatusConst = Status.UNDEFINED
        self.wps = []
        self.end = LongDurationJustificationDAO._getEnd(self, days)

    def persist(self, con, days=None):

        jid = LongDurationJustificationDAO.persist(con, self, days)
        s = Status(jid,self.ownerId)
        s.created = s.created - datetime.timedelta(seconds=1)
        sid = s.persist(con)

        self.status = s
        self.statusId = s.id
        self.statusConst = s.status

        self.changeStatus(con, Status.APPROVED, self.ownerId)

        return jid

    def changeStatus(self, con, status, userId):
        assert status is not None
        assert (self.status is not None or self.statusId is not None)

        if self.status == None:
            self.status = Status.findByIds(con, [self.statusId])
        else:
            self.statusId = self.status.id

        self.status.changeStatus(con, self, status, userId)

    def _getLastStatus(self, con):
        if self.status is None:
            self.status = Status.getLastStatus(con, self.id)
            self.statusId = self.status.id
            self.statusConst = self.status.status

        return self.status

    def _loadWorkedPeriods(self, wps):
        assert self.status is not None

        if self.status.status != Status.APPROVED:
            return

        for wp in wps:
            if self.start <= wp.date <= self.end:
                self.wps.append(wp)
                wp.addJustification(self)

    @classmethod
    def findByUserId(cls,con, userIds, start, end):
        return LongDurationJustificationDAO.findByUserId(con, userIds, start, end)

    @classmethod
    def findById(cls, con, ids):
        return LongDurationJustificationDAO.findById(con, ids)


class LongDurationJustificationDAO:
    registry = inject.instance(Registry).getRegistry('longDurationJustification')

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;
                create table assistance.long_duration_j (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    owner_id varchar not null references profile.users (id),
                    jstart date default now(),
                    jend date default now(),
                    number bigint,
                    created timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        j = LongDurationJustification(r['user_id'], r['owner_id'], r['jstart'], 0, r['number'])
        j.id = r['id']
        j.end = r['jend']

        return j

    @staticmethod
    def _getEnd(j, days):
        if j.start is None:
            return None

        continuous = LongDurationJustificationDAO.registry.get('continuousDays')
        if (continuous.lower() == 'true'):
            return j.start + datetime.timedelta(days=days)
        else:
            date = j.start
            while (days > 0):
                if date.weekday() >= 5:
                    date = date + datetime.timedelta(days = (7 - date.weekday()))
                else:
                    days = days - 1
                    date = date + datetime.timedelta(days=1)

            if date.weekday() >= 5:
                date = date + datetime.timedelta(days = (7 - date.weekday()))
            return date

    def _verifyConstraints(j, days):
        '''
        debe verificar que no supere el limite anual de justificaciones
        '''
        return

    @staticmethod
    def persist(con, j, days):
        assert j is not None

        cur = con.cursor()
        try:
            if ((not hasattr(j, 'id')) or (j.id is None)):
                j.id = str(uuid.uuid4())

                r = j.__dict__
                cur.execute('insert into assistance.long_duration_j (id, user_id, owner_id, jstart, jend, number) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(number)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.long_duration_j set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s, number = %(number)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @staticmethod
    def findById(con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.long_duration_j where id in %s',tuple(ids))
            return [ LongDurationJustificationDAO._fromResult(r) for r in cur ]
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
            cur.execute('select * from assistance.long_duration_j where user_id in %s and '
                        '((jend >= %s and jend <= %s) or '
                        '(jstart >= %s and jstart <= %s) or '
                        '(jstart <= %s and jend >= %s))', (tuple(userIds), sDate, eDate, sDate, eDate, sDate, eDate))

            return [ LongDurationJustificationDAO._fromResult(r) for r in cur ]
        finally:
            cur.close()
