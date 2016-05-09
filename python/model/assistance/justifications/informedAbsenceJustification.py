
from model.assistance.assistanceDao import AssistanceDAO
from model.assistance.justifications.justifications import Justification
from model.assistance.justifications.status import Status
from model.assistance.justifications.justifications import SingleDateJustification
from model.users.users import UserDAO

import datetime, uuid


class InformedAbsenceJustificationDAO(AssistanceDAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)

        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS assistance;

              create table IF NOT EXISTS assistance.justification_informed_absence (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    owner_id varchar not null references profile.users (id),
                    jdate date default now(),
                    created timestamptz default now()
              );
              """
            cur.execute(sql)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, con, r):
        j = InformedAbsenceJustification()
        j.id = r['id']
        j.userId = r['user_id']
        j.ownerId = r['owner_id']
        j.date = r['jdate']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j

    @classmethod
    def persist(cls, con, j):
        assert con is not None
        assert j is not None

        cur = con.cursor()
        try:
            if not hasattr(j, 'id') or j.id is None:
                j.id = str(uuid.uuid4())

            if len(j.findById(con, [j.id])) <=  0:
                r = j.__dict__
                cur.execute('insert into assistance.justification_informed_absence(id, user_id, owner_id, jdate) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(date)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_informed_absence set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jdate = %(date)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.justification_informed_absence where id in %s', (tuple(ids),))
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
            cur.execute('select * from assistance.justification_informed_absence where user_id  in %s and jdate BETWEEN %s AND %s', (tuple(userIds), start, eDate))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

class InformedAbsenceJustification(SingleDateJustification):

    dao = InformedAbsenceJustificationDAO

    def __init__(self, date = None, userId = None, ownerId = None):
        super().__init__(date, userId, ownerId)
        self.identifier = "Ausente con aviso"
        self.classType = SingleDateJustification.__name__

    def getIdentifier(self):
        return self.identifier

    @classmethod
    def create(cls, con, date, userId, ownerId):
        cls._checkConstraints(con, date, userId)
        return super().create(con, date, userId, ownerId)

    @classmethod
    def _checkConstraints(cls, con, date, userId):
        """
            Se controla:
                6 anuales
                2 mensuales
        """
        yearStart = Utils._cloneDate(date).replace(month=1,day=1)
        yearEnd = Utils._cloneDate(date).replace(month=12,day=31)
        justs = cls.dao.findByUserId(con, [userId], yearStart, yearEnd)
        if len(justs) >= 6:
            raise Exception('Límite anual alcanzado')

        actualMonth = date.month
        if len([j for j in justs if j.getDate().month == actualMonth]) >= 2:
            raise Exception('Límite mensual alcanzado')
