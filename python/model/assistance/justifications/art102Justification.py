# -*- coding: utf-8 -*-

from model.assistance.assistanceDao import AssistanceDAO
from model.users.users import UserDAO

from model.assistance.justifications.justifications import SingleDateJustification
from model.assistance.justifications.status import Status
from model.assistance.justifications.status import StatusDAO
from model.assistance.utils import Utils
import uuid, datetime

class Art102JustificationDAO(AssistanceDAO):

    dependencies = [UserDAO, StatusDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_art102 (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    owner_id varchar not null references profile.users (id),
                    date date not null default now(),
                    notes varchar,
                    created timestamptz default now()
              );
              """
            cur.execute(sql)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, con, r):
        c = Art102Justification()
        c.id = r['id']
        c.userId = r['user_id']
        c.ownerId = r['owner_id']
        c.date = r['date']
        c.notes = r['notes']
        c.setStatus(Status.getLastStatus(con, c.id))
        return c

    @classmethod
    def persist(cls, con, c):
        assert c is not None

        cur = con.cursor()
        try:
            if ((not hasattr(c, 'id')) or (c.id is None)):
                c.id = str(uuid.uuid4())

            if len(c.findById(con, [c.id])) <=  0:

                r = c.__dict__
                cur.execute('insert into assistance.justification_art102 (id, user_id, owner_id, date, notes) '
                            'values ( %(id)s, %(userId)s, %(ownerId)s, %(date)s, %(notes)s)', r)
            else:
                r = c.__dict__
                cur.execute('update assistance.justification_art102 set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'date = %(date)s, , notes = %(notes)s where id = %(id)s', r)
            return c.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_art102 where id in %s', (tuple(ids),))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

    @classmethod
    def findByUserId(cls, con, userIds, start, end):
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.date)
        assert isinstance(end, datetime.date)

        if len(userIds) <= 0:
            return

        cur = con.cursor()
        try:
            eDate = datetime.date.today() if end is None else end
            cur.execute('select * from assistance.justification_art102 where user_id  in %s and date BETWEEN %s AND %s', (tuple(userIds), start, eDate))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

class Art102Justification(SingleDateJustification):

    dao = Art102JustificationDAO
    indentifier = "Artículo 102"

    def __init__(self, date = None, userId = None, ownerId = None):
        super().__init__(date, userId, ownerId)
        self.identifier = Art102Justification.indentifier
        self.classType = SingleDateJustification.__name__

    def getIdentifier(self):
        return self.indentifier

    @classmethod
    def create(cls, con, date, userId, ownerId):
        cls._checkConstraints(con, date, userId)
        return super().create(con, date, userId, ownerId)

    @classmethod
    def _getYearJustifications(cls, con, date, userId):
        yearStart = Utils._cloneDate(date).replace(month=1,day=1)
        yearEnd = Utils._cloneDate(date).replace(month=12,day=31)
        justs = cls.dao.findByUserId(con, [userId], yearStart, yearEnd)
        return [j for j in justs if j.getStatus().status == 1 or j.getStatus().status == 2]

    @classmethod
    def _checkConstraints(cls, con, date, userId):
        """
            Se controla:
                5 anuales
        """
        justs = cls._getYearJustifications(con, date, userId)
        if len(justs) >= 5:
            raise Exception('Límite anual alcanzado')

    @classmethod
    def getData(cls, con, userId, date, schedule):
        data = super().getData(con, userId, date, schedule)
        justs = cls._getYearJustifications(con, date, userId)
        data['stock'] = 5 - len(justs)
        return data
