
from model.dao import DAO
from model.assistance.justifications.justifications import Justification


class InformedAbsenceDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;
                create table assistance.justification_informed_absence (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    owner_id varchar not null references profile.users (id),
                    jdate date default now(),
                    created timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(con, r):
        j = InformedAbsenceJustification(r['user_id'], r['owner_id'], r['jstart'], 0, r['number'])
        j.id = r['id']
        j.end = r['jdate']
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
                cur.execute('insert into assistance.justification_informed_absence(id, user_id, owner_id, jdate) '
                            'values (%(id)s, %(userId)s, %(ownerId)s, %(date)s)', r)
            else:
                r = j.__dict__
                cur.execute('update assistance.justification_informed_absence set user_id = %(userId)s, owner_id = %(ownerId)s, '
                            'jdate = %(date)s where id = %(id)s', r)
            return j.id

        finally:
            cur.close()



class InformedAbsenceJustification(SingleDateJustification):

    def __init__(self, userId, ownerId, date):
        super().__init__(date, userId, ownerId)

    def getIdentifier(self):
        return "Ausente con aviso"
