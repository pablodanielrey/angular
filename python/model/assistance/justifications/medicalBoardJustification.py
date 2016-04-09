# -*- coding: utf-8 -*-
'''
    implementa la justificación de corta duración
    dentro del registry debe existir una sección :

    [medicalBoardJustification]
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

class MedicalBoardJustification(RangedJustification):

    registry = inject.instance(Registry).getRegistry('medicalBoardJustification')

    def __init__(self, userId, ownerId, start, days = 0, number = None):
        super().__init__(start, userId, ownerId)
        if (MedicalBoardJustification.registry.get('continuousDays').lower == 'true'):
            self.end = self._getEnd(start, days, True)
        else:
            self.end = self._getEnd(start, days, False)
        self.number = number

    def getIdentifier(self):
        return 'Junta médica'

    def persist(self, con):
        jid = MedicalBoardJustificationDAO.persist(con, self)

        s = Status(jid, self.ownerId)
        s.created = s.created - datetime.timedelta(seconds=1)
        sid = s.persist(con)

        self.status = s
        self.statusId = s.id
        self.statusConst = s.status

        self.changeStatus(con, Status.APPROVED, self.ownerId)

        return jid

    #def changeStatus(self, con, status, userId = None):
    #    super().changeStatus(con,status,userId)


    #def _getLastStatus(self, con):
    #    super()._getLastStatus(con)

    @classmethod
    def findByUserId(cls,con, userIds, start, end):
        return MedicalBoardJustificationDAO.findByUserId(con, userIds, start, end)

    @classmethod
    def findById(cls, con, ids):
        return MedicalBoardJustificationDAO.findById(con, ids)


class MedicalBoardJustificationDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;
                create table assistance.medical_board_j (
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
    def _fromResult(con, r):
        j = MedicalBoardJustification(r['user_id'], r['owner_id'], r['jstart'], 0, r['number'])
        j.id = r['id']
        j.end = r['jend']

        j.status = Status.getLastStatus(con, j.id)
        j.statusId = j.status.id
        j.statusConst = j.status.status

        return j

    @staticmethod
    def persist(con, j):
        assert j is not None

        cur = con.cursor()
        try:
            if ((not hasattr(j, 'id')) or (j.id is None)):
                j.id = str(uuid.uuid4())

                r = j.__dict__
                cur.execute('insert into assistance.medical_board_j (id, user_id, owner_id, jstart, jend, number) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(number)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.medical_board_j set user_id = %(userId)s, owner_id = %(ownerId)s, '
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
            cur.execute('select * from assistance.medical_board_j where id in %s',(tuple(ids),))
            return [ MedicalBoardJustificationDAO._fromResult(con, r) for r in cur ]
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
            cur.execute('select * from assistance.medical_board_j where user_id in %s and '
                        '((jend >= %s and jend <= %s) or '
                        '(jstart >= %s and jstart <= %s) or '
                        '(jstart <= %s and jend >= %s))', (tuple(userIds), sDate, eDate, sDate, eDate, sDate, eDate))

            return [ MedicalBoardJustificationDAO._fromResult(con, r) for r in cur ]
        finally:
            cur.close()
