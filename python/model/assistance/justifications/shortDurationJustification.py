# -*- coding: utf-8 -*-
'''
    implementa la justificación de corta duración
    dentro del registry debe existir una sección :

    [shortDurationJustification]
    continuousDays = True

'''
from model.connection.connection import Connection
from model.registry import Registry
from model.serializer.utils import JSONSerializable
import inject, logging


from model.assistance.justifications.justifications import Justification
from model.assistance.justifications.status import Status
import datetime, uuid

class ShortDurationJustification(JSONSerializable, Justification):

    def __init__(self):
        self.id = None
        self.userId = None
        self.ownerId = None
        self.start = None
        self.end = None
        self.number = 0
        self.status = None
        self.statusId = None
        self.statusConst = Status.UNDEFINED


    def persist(self, con, days=None):

        jid = ShortDurationJustificationDAO.persist(con, self, days)
        s = Status(jid,self.ownerId)
        s.created = s.created - datetime.timedelta(seconds=1)
        sid = s.persist(con)

        self.status = s
        self.statusId = s.id
        self.statusConst = s.status

        self.changeStatus(con, Status.APPROVED, self.ownerId)

        return jid

    def changeStatus(self, con, status, userId):
        if self.status == None and self.statusId == None:
            return
        if self.status == None:
            self.status = Status.findByIds(con, [self.statusId])

        self.status = self.status.changeStatus(con, status, userId)
        self.statusId = self.status.id
        self.statusConst = self.status.status

    def getLastStatus(self, con):
        self.status = Status.getLastStatus(con, self.id)
        self.statusId = self.status.id
        self.statusConst = self.status.status

        return self.status

    @classmethod
    def findByUserId(cls,con, userIds, start, end):
        return ShortDurationJustificationDAO.findByUserId(con, userIds, start, end)

    @classmethod
    def findById(cls, con, ids):
        return ShortDurationJustificationDAO.findById(con, ids)


class ShortDurationJustificationDAO:
    registry = inject.instance(Registry).getRegistry('shortDurationJustification')

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;
                create table assistance.short_duration_j (
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
        j = ShortDurationJustification()
        j.id = r['id']
        j.userId = r['user_id']
        j.ownerId = r['owner_id']
        j.start = r['jstart']
        j.end = r['jend']
        j.number = r['number']

        return j

    @staticmethod
    def _getEnd(j, days):
        if j.start is None:
            return None

        continuous = ShortDurationJustificationDAO.registry.get('continuousDays')
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
        cur = con.cursor()
        try:
            ShortDurationJustificationDAO._verifyConstraints(j, days)

            if j.end is None:
                j.end = ShortDurationJustificationDAO._getEnd(j, days)

            if ((not hasattr(j, 'id')) or (j.id is None)):
                j.id = str(uuid.uuid4())

                r = j.__dict__
                cur.execute('insert into assistance.short_duration_j (id, user_id, owner_id, jstart, jend, number) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(number)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.short_duration_j set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s, number = %(number)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @staticmethod
    def findById(con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            logging.info('ids: %s', tuple(ids))
            cur.execute('select * from assistance.short_duration_j where id in %s',(tuple(ids),))
            return [ ShortDurationJustificationDAO._fromResult(r) for r in cur ]
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
            cur.execute('select * from assistance.short_duration_j where user_id in %s and '
                        '((jend >= %s and jend <= %s) or '
                        '(jstart >= %s and jstart <= %s) or '
                        '(jstart <= %s and jend >= %s))', (tuple(userIds), sDate, eDate, sDate, eDate, sDate, eDate))

            return [ ShortDurationJustificationDAO._fromResult(r) for r in cur ]
        finally:
            cur.close()
