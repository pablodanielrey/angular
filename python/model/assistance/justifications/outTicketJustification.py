# -*- coding: utf-8 -*-
import logging
import datetime
import dateutil
import uuid


from model.assistance.justifications.justifications import Justification, RangedJustification, RangedTimeJustification
from model.assistance.justifications.status import Status
from model.assistance.justifications.status import StatusDAO

from model.assistance.assistanceDao import AssistanceDAO
from model.users.users import UserDAO
from model.assistance.utils import Utils

class OutTicketJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO, StatusDAO]

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
                    notes varchar,
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
                cur.execute('insert into assistance.justification_out_ticket (id, user_id, owner_id, jstart, jend, type, notes) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(start)s, %(end)s, %(type)s, %(notes)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_out_ticket set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jstart = %(start)s, jend = %(end)s, type = %(type)s, notes = %(notes)s where id = %(id)s', r)
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
        assert isinstance(start, datetime.date)
        assert isinstance(end, datetime.date)

        if len(userIds) <= 0:
            return

        cur = con.cursor()
        try:
            t = cls.type
            eDate = datetime.date.today() if end is None else end
            cur.execute('select * from assistance.justification_out_ticket where user_id in %s and (jstart <= %s and jend >= %s) and type = %s', (tuple(userIds), eDate, start, t))
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
        j.notes = r['notes']
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
        j.notes = r['notes']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j


class OutTicketJustification(RangedTimeJustification):

    def __init__(self, start = None, end=None, userId = None, ownerId = None):
        super().__init__(start, end, userId, ownerId)
        self.typeName = 'Boleta de salida'
        self.classType = RangedTimeJustification.__name__

    @classmethod
    def create(cls, con, start, end, userId, ownerId):
        assert con is not None
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)

        cls._checkConstraints(con, start, end, userId)
        return super().create(con, start, end, userId, ownerId)

    @classmethod
    def _getJustifiedTime(cls, justs):
        diffSum = 0
        for j in justs:
            diffSum = diffSum + j.getJustifiedSeconds()
        return diffSum

    @classmethod
    def _getMonthJustifications(cls, con, date, userId):
        monthStart = Utils._cloneDate(date).replace(day=1, hour=0, minute=0, second=0)
        from calendar import monthrange
        (dstart, dend) = monthrange(monthStart.year, monthStart.month)
        monthEnd = Utils._cloneDate(monthStart) + datetime.timedelta(days=dend) - datetime.timedelta(seconds=1)
        justs = cls.dao.findByUserId(con, [userId], monthStart, monthEnd)
        return [j for j in justs if j.getStatus().status == 1 or j.getStatus().status == 2]

    @classmethod
    def _getAllMonthJustifications(cls, con, date, userId):
        justs = []
        for c in OutTicketJustification.__subclasses__():
            justs.extend(c._getMonthJustifications(con, date, userId))
        return justs

    @classmethod
    def _checkConstraints(cls, con, start, end, userId):
        assert start < end
        """ chequeo cantidad de horas pedidas """
        diff = (end - start).seconds
        limitSeconds = 3 * 60 * 60

        if diff > limitSeconds:
            raise Exception('El tiempo requerido supera el límite')

        '''
        if diff < 60 * 60:
            raise Exception('Como mínimo se debe pedir 1 hora')
        '''
        
        justs = cls._getAllMonthJustifications(con, start, userId)
        diffSum = cls._getJustifiedTime(justs)
        if diff > (limitSeconds - diffSum):
            raise Exception('Supera las horas disponibles')

    @classmethod
    def getData(cls, con, userId, date, schedule):
        data = super().getData(con, userId, date, schedule)
        justs = cls._getAllMonthJustifications(con, date, userId)
        diffSum = cls._getJustifiedTime(justs)

        limitSeconds = 3 * 60 * 60
        totalSum = limitSeconds - diffSum
        for i in range(date.month + 1, 13):
            d = Utils._cloneDate(date).replace(month=i)
            j = cls._getAllMonthJustifications(con, d, userId)
            diff = cls._getJustifiedTime(j)
            totalSum = totalSum + (limitSeconds - diff)

        data['yStock'] = totalSum
        data['mStock'] = limitSeconds - diffSum
        return data

class OutTicketWithReturnJustification(OutTicketJustification):

    dao = OutTicketWithReturnJustificationDAO

    def __init__(self, start = None, end=None, userId = None, ownerId = None):
        super().__init__(start, end, userId, ownerId)
        self.identifier = "con retorno"

    def getIdentifier(self):
        return self.typeName + " " + self.identifier

    def changeEnd(self, con, end):
        self.end = end
        OutTicketWithReturnJustificationDAO.persist(con)


class OutTicketWithoutReturnJustification(OutTicketJustification):

    dao = OutTicketWithoutReturnJustificationDAO

    def __init__(self, start = None, end = None, userId = None, ownerId = None):
        super().__init__(start, end, userId, ownerId)
        self.identifier = "sin retorno"

    def getIdentifier(self):
        return self.typeName + " " + self.identifier

    def _loadWorkedPeriods(self, wps):
        assert self.getStatus() is not None
        if self.getStatus().status != Status.APPROVED:
            return

        for wp in wps:
            logging.debug("{} == {} and {} >= {}".format(wp.date, self.start.date(), wp.getEndDate(), self.start))
            if wp.date == self.start.date() and  wp.getEndDate() >= self.start:
                self.wps.append(wp)
                wp.addJustification(self)
