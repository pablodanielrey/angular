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
import inject


from model.assistance.justifications.status import Status
import datetime, uuid

class ShortDurationJustification(JSONSerializable):
    prefix = '0001'

    def __init__(self):
        self.id = None
        self.userId = None
        self.owner = None
        self.start = None
        self.end = None
        self.number = 0
        self.status = None
        self.statusId = None
        self.statusConst = Status.UNDEFINED


    def persist(self, con, days=None):
        jid = ShortDurationJustificationDAO.persist(con, self, days)
        s = Status(jid,self.owner)
        sid = s.persist(con)
        s.status = Status.APPROVED
        s.created = s.created + datetime.timedelta(seconds = 1)
        sid = s.persist(con)

        self.status = s
        self.statusId = sid
        self.statusConst = s.status
        return jid

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
                    owner varchar not null references profile.users (id),
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
        j.owner = r['owner']
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


    @staticmethod
    def persist(con, j, days):
        cur = con.cursor()
        try:
            if j.end is None:
                j.end = ShortDurationJustificationDAO._getEnd(j, days)

            if hasattr(j, 'id') or j.id is None:
                j.id = ShortDurationJustification.prefix + "-" + str(uuid.uuid4())

                r = j.__dict__
                cur.execute('insert into assistance.short_duration_j (id, user_id, owner, jstart, jend, number) '
                            'values (%(id)s, %(userId)s, %(owner)s, %(start)s, %(end)s, %(number)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.short_duration_j set user_id = %(userId)s, owner = %(owner)s, '
                            'jstart = %(start)s, jend = %(end)s, number = %(number)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @staticmethod
    def findById(con, ids):
        assert isinstance(ids, list)

        pass

    @staticmethod
    def findBy(con, userId, startData, endDate):
        pass
