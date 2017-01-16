# -*- coding: utf-8 -*-
import uuid

from model.dao import SqlDAO
from model.designation.entities.designation import Designation

class DesignationSqlDAO(SqlDAO):
    ''' DAO designation '''

    dependencies = [UsersSqlDAO, PlaceSqlDAO, PositionsSqlDAO]
    _schema = "designations."
    _table = "designation"
    _entity = Designation
    _mappings = {
        'start':'dstart',
        'end':'dend',
    }

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(con)
        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS designations.designation (
                    id VARCHAR PRIMARY KEY,
                    type VARCHAR NOT NULL,

                    user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                    place_id VARCHAR REFERENCES designations.place (id),
                    position_id VARCHAR REFERENCES designations.positions (id),
                    parent_id VARCHAR REFERENCES designations.designation (id),
                    original_id VARCHAR REFERENCES designations.designation (id),

                    created timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, d, r):
        d.id = r['id']
        d.start = r['dstart']
        d.end = r['dend']
        d.type = r["type"]
        d.parentId = r["parent_id"]
        d.originalId = r["original_id"]
        d.placeId = r['place_id']
        d.positionId = r['position_id']
        d.userId = r['user_id']

        return d

    @classmethod
    def deleteByIds(cls, ctx, ids):
        assert ids is not None
        assert isinstance(ids, list)
        cur = ctx.con.cursor()
        try:
            cur.execute('update designations.designation set dend = NOW() where id in %s', (tuple(ids),))
        finally:
            cur.close()

    @classmethod
    def persist(cls, ctx, desig):
        cur = ctx.con.cursor()
        try:
            if not hasattr(desig, 'id'):
                desig.id = str(uuid.uuid4())
            cur.execute("insert into designations.designation (id, place_id, user_id, position_id, dstart, dend) "
                        "values (%(id)s, %(placeId)s, %(userId)s, %(positionId)s, %(start)s, %(end)s)",
                        desig.__dict__)
            return desig.id
        finally:
            cur.close()
