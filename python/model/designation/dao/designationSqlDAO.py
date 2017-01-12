# -*- coding: utf-8 -*-
import uuid

from model.dao import SqlDAO
from model.designation.entities.designation import Designation

class DesignationSqlDAO(SqlDAO):
    ''' DAO designation '''

    _schema = "designations."
    _table = "designation"
    _entity = Designation
    _mappings = {
                'start':'dstart',
                'end':'dend',
                'out':'dout'
            }

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

    @classmethod
    def _fromResult(cls, d, r):
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
    def expireByIds(cls, ctx, ids):
        assert ids is not None
        assert isinstance(ids, list)
        cur = ctx.con.cursor()
        try:
            cur.execute('update designations.designation set dout = NOW() where id in %s', (tuple(ids),))
        finally:
            cur.close()


    @classmethod
    def persist(cls, ctx, desig):
        cur = ctx.con.cursor()
        try:
            if not hasattr(desig, 'id'):
                desig.id = str(uuid.uuid4())
            cur.execute("insert into designations.designation (id, office_id, user_id, position_id, dstart, dend) "
                        "values (%(id)s, %(officeId)s, %(userId)s, %(positionId)s, %(start)s, %(end)s)",
                        desig.__dict__)
            return desig.id
        finally:
            cur.close()
