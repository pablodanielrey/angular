# -*- coding: utf-8 -*-
import logging
import datetime
import uuid


from model.assistance.justifications.justifications import Justification, RangedJustification
from model.assistance.justifications.status import Status


class OutputTicketDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;
                create table assistance.justification_output_ticket (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    owner_id varchar not null references profile.users (id),
                    jstart timestamptz default now(),
                    jend timestamptz default now(),
                    created timestamptz default now()
                );
            """.format(OutputTicketDAO.TABLE_NAME))
        finally:
            cur.close()

    @staticmethod
    def _fromResult(con, r):
        j = OutputTicket(r['user_id'], r['owner_id'], r['jstart'], r['jend'])
        j.id = r['id']
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
                cur.execute('insert into assistance.justification_output_ticket (id, user_id, owner_id, jstart, jend) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_output_ticket set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @staticmethod
    def findById(con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.output_ticket where id in %s', (tuple(ids),))
            return [ OutputTicketDAO._fromReuslt(con, r) for r in cur ]
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
            cur.execute('select * from assistance.justification_output_ticket where user_id in %s and '
                        '((jend >= %s and jend <= %s) or '
                        '(jstart >= %s and jstart <= %s) or '
                        '(jstart <= %s and jend >= %s))', (tuple(userIds), start, end, start, end, start, end))

            return [ OutputTicketDAO._fromResult(con, r) for r in cur ]
        finally:
            cur.close()


class OutputTicket(RangedJustification):

    dao = OutputTicketDAO

    def __init__(self, userId, ownerId, start, end):
        super().__init__(start, 0, userId, ownerId)
        self.end = end

    def getIdentifier(self):
        return 'Boleta de Salida'
