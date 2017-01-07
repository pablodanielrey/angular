# -*- coding: utf-8 -*-
from model.designation.designation import DesignationDAO, Designation

class DesignationSqlDAO(DesignationDAO):
    _schema = "designations."
    _table = "designation"

    @classmethod
    def prueba(cls, con):
        print('prueba')
        print(con.__dict__)


    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con['con'].cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS designations.designation (
                    id VARCHAR PRIMARY KEY,
                    user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                    office_id VARCHAR REFERENCES offices.offices (id),
                    position_id VARCHAR REFERENCES designations.positions (id),
                    parent_id VARCHAR REFERENCES designations.designation (id),
                    original_id VARCHAR REFERENCES designations.designation (id),

                    dstart DATE default now(),
                    dend DATE,
                    dout DATE,
                    description VARCHAR NOT NULL,
                    resolution VARCHAR,
                    record VARCHAR,

                    old_id INTEGER NOT NULL,
                    old_type VARCHAR NOT NULL,
                    old_resolution_out VARCHAR,
                    old_record_out VARCHAR,

                    created timestamptz default now()
                );
            """)
        except Error:
          print("error")
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        d = Designation()
        d.id = r['id']
        d.start = r['dstart']
        d.end = r['dend']
        d.out = r["dout"]
        d.description = r["description"]
        d.resolution = r["resolution"]
        d.record = r["record"]
        d.replaceId = r["parent_id"]
        d.originalId = r["original_id"]
        d.officeId = r['office_id']
        d.positionId = r['position_id']
        d.userId = r['user_id']

        return d

    @classmethod
    def expireByIds(cls, con, ids):
        assert ids is not None
        assert isinstance(ids, list)
        cur = con['con'].cursor()
        try:
            cur.execute('update designations.designation set dout = NOW() where id in %s', (tuple(ids),))
        finally:
            cur.close()

    @classmethod
    def findByUsers(cls, con, userIds, history=False):
        assert userIds is not None
        assert isinstance(userIds, list)
        cur = con['con'].cursor()
        try:
            if history is None or not history:
                cur.execute('select id from designations.designation where user_id IN %s and dout is null order by dstart',(tuple(userIds),))
            else:
                cur.execute('select id from designations.designation where user_id IN %s order by dstart',(tuple(userIds),))
            return [d['id'] for d in cur]
        finally:
            cur.close()

    @classmethod
    def findByPlaces(cls, con, placeIds, history=False):
        if not history:
            cond = {"office_id":placeIds, "dout":"NULL"}
        else:
            cond = {"office_id":placeIds}
        return cls.findByFields(con, cond, {"dstart":"asc"})

    @classmethod
    def findByIds(cls, con, ids):
        assert ids is not None
        assert isinstance(ids, list)

        if len(ids) <= 0:
            return []

        cur = con['con'].cursor()
        try:
            cur.execute('select * from designations.designation where id in %s order by dstart asc', (tuple(ids),))
            if cur.rowcount <= 0:
                return []

            return [cls._fromResult(d) for d in cur.fetchall()]

        finally:
            cur.close()

    @classmethod
    def findByOffice(cls, con, officeId, history=False):
        if history:
            cond = {"office_id":[officeId], "dout":"IS NOT NULL"}
        else:
            cond = {"office_id":[officeId]}

        return cls.findByFields(con, cond, {"dstart":"asc"})

    @classmethod
    def persist(cls, con, desig):
        cur = con['con'].cursor()
        try:
            if not hasattr(desig, 'id'):
                desig.id = str(uuid.uuid4())
            cur.execute("insert into designations.designation (id, office_id, user_id, position_id, dstart, dend) "
                        "values (%(id)s, %(officeId)s, %(userId)s, %(positionId)s, %(start)s, %(end)s)",
                        desig.__dict__)
            return desig.id
        finally:
            cur.close()
