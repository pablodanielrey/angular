
from model.assistance.assistanceDao import AssistanceDAO
from model.assistance.justifications.justifications import Justification
from model.assistance.justifications.status import Status
from model.assistance.justifications.justifications import SingleDateJustification
from model.users.users import UserDAO

import datetime


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
        date = datetime.datetime.combine(r['jdate'], datetime.time.min)
        j = InformedAbsenceJustification(r['user_id'], r['owner_id'], date)
        j.id = r['id']
        j.setStatus(Status.getLastStatus(con, j.id))
        return j

    @classmethod
    def persist(cls, con, j):
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
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)

        if len(userIds) <= 0:
            return

        cur = con.cursor()
        try:
            sDate = None if start is None else start.date()
            eDate = datetime.date.today() if end is None else end.date()
            cur.execute('select * from assistance.justification_informed_absence where user_id  in %s and jdate BETWEEN %s AND %s', (tuple(userIds), sDate, eDate))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()

class InformedAbsenceJustification(SingleDateJustification):

    dao = InformedAbsenceJustificationDAO
    identifier = "Ausente con aviso"

    def __init__(self, userId = None, ownerId = None, date = None):
        super().__init__(date, userId, ownerId)
        self.identifier = InformedAbsenceJustification.identifier
        self.classType = SingleDateJustification.__name__

    def getIdentifier(self):
        return self.identifier
