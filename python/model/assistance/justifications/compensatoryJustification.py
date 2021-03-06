# -*- coding: utf-8 -*-

from model.assistance.justifications.justifications import SingleDateJustification
from model.assistance.justifications.status import Status
from model.assistance.justifications.status import StatusDAO
import uuid, datetime

from model.assistance.assistanceDao import AssistanceDAO
from model.users.users import UserDAO

class CompensatoryJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO, StatusDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_compensatory (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    owner_id varchar not null references profile.users (id),
                    date date not null default now(),
                    notes varchar,
                    created timestamptz default now()
              );

              CREATE TABLE IF NOT EXISTS assistance.justification_compensatory_stock (
                    user_id varchar primary key references profile.users (id),
                    stock bigint default 0,
                    updated timestamptz default now()
              );
              """
            cur.execute(sql)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, con, r):
        c = CompensatoryJustification()
        c.id = r['id']
        c.date = r['date']
        c.userId = r['user_id']
        c.ownerId = r['owner_id']
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
                cur.execute('insert into assistance.justification_compensatory (id, user_id, owner_id, date, notes) '
                            'values ( %(id)s, %(userId)s, %(ownerId)s, %(date)s, %(notes)s)', r)
            else:
                r = c.__dict__
                cur.execute('update assistance.justification_compensatory set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'date = %(date)s, notes = %(notes)s where id = %(id)s', r)
            return c.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_compensatory where id in %s', (tuple(ids),))
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
            cur.execute('select * from assistance.justification_compensatory where user_id  in %s and date BETWEEN %s AND %s', (tuple(userIds), start, eDate))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

    @classmethod
    def getStock(cls, con, userId):
        cur = con.cursor()
        try:
            cur.execute('select stock from assistance.justification_compensatory_stock where user_id = %s', (userId,))
            if cur.rowcount <= 0:
                return 0
            else:
                return cur.fetchone()['stock']
        finally:
            cur.close()

    @classmethod
    def updateStock(cls, con, userId, stock, updated = None):
        cur = con.cursor()
        try:
            cur.execute('delete from assistance.justification_compensatory_stock where user_id = %s', (userId,))

            if updated is None:
                cur.execute('insert into assistance.justification_compensatory_stock (user_id, stock) '
                            'values ( %s, %s)', (userId, stock))

            else:
                cur.execute('insert into assistance.justification_compensatory_stock (user_id, stock, updated) '
                            'values ( %s, %s, %s)', (userId, stock, updated))
        finally:
            cur.close()

class CompensatoryJustification(SingleDateJustification):

    dao = CompensatoryJustificationDAO
    identifier = "Compensatorio"

    def __init__(self, date = None, userId = None, ownerId = None):
        super().__init__(date, userId, ownerId)
        self.identifier = CompensatoryJustification.identifier
        self.classType = SingleDateJustification.__name__

    def getIdentifier(self):
        return self.identifier

    @classmethod
    def create(cls, con, date, userId, ownerId):
        if cls.getStock(con, userId) <= 0:
            raise Exception('No tiene compensatorios')
        return super().create(con, date, userId, ownerId)

    @classmethod
    def getStock(cls, con, userId):
        return cls.dao.getStock(con, userId)

    @classmethod
    def updateStock(cls, con, userId, stock, calculated = None):
        return cls.dao.updateStock(con, userId, stock, calculated)

    @classmethod
    def getData(cls, con, userId, date, schedule):
        data = super().getData(con, userId, date, schedule)
        data['stock'] = cls.getStock(con, userId)
        return data

    def persist(self, con):
        super().persist(con)
        self.dao.updateStock(con, self.userId, CompensatoryJustification.getStock(con, self.userId) - 1)

    def changeStatus(self, con, statusConst, userId):
        old = self.getStatus()
        super().changeStatus(con, statusConst, userId)
        assert self.getStatus().status == statusConst

        '''
            si estaba como pendiente o aprobado y pasa otro estado tengo que sumar uno al stock
        '''
        if ((old.status == Status.PENDING or old.status == Status.APPROVED) and
            (self.getStatus().status != Status.PENDING and self.getStatus().status != Status.APPROVED)):
            self.dao.updateStock(con, userId, CompensatoryJustification.getStock(con, userId) + 1)
            return

        '''
            si no estaba como pendiente ni aprobado y pasa a alguno de estos estados decremento uno
        '''
        if ((old.status != Status.PENDING and old.status != Status.APPROVED) and
        (self.getStatus().status == Status.PENDING and self.getStatus().status == Status.APPROVED)):
            stock = CompensatoryJustification.getStock(con, userId) - 1
            self.dao.updateStock(con, userId, 0 if stock < 0 else stock)
            return
