# -*- coding: utf-8 -*-
import uuid

from model.dao import SqlDAO
from model.users.dao.userSqlDAO import UserSqlDAO
from model.designation.dao.placeSqlDAO import PlaceSqlDAO
from model.designation.dao.positionSqlDAO import PositionSqlDAO
from model.designation.entities.designation import Designation

class DesignationSqlDAO(SqlDAO):
    ''' DAO designation '''

    dependencies = [UserSqlDAO, PlaceSqlDAO, PositionSqlDAO]
    _schema = "designations."
    _table = "designation_"
    _entity = Designation
    _mappings = {
        'start':'dstart',
        'end':'dend',
    }

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)
        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS designations.designation_ (
                    id VARCHAR PRIMARY KEY,
                    type VARCHAR,

                    dstart DATE,
                    dend DATE,

                    user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                    place_id VARCHAR REFERENCES designations.place (id),
                    position_id VARCHAR REFERENCES designations.position (id),
                    parent_id VARCHAR REFERENCES designations.designation_ (id),
                    start_id VARCHAR REFERENCES designations.designation_ (id),

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
        d.startId = r["start_id"]
        d.placeId = r['place_id']
        d.positionId = r['position_id']
        d.userId = r['user_id']

        return d


    @classmethod
    def persist(cls, ctx, entity):
        ''' inserta o actualiza una oficia '''
        cur = ctx.con.cursor()
        try:

            if not hasattr(entity, 'id') or entity.id is None:
                entity.id = str(uuid.uuid4())
                cur.execute("insert into designations.designation_ (id, place_id, user_id, position_id, dstart, dend, type) "
                            "values (%(id)s, %(placeId)s, %(userId)s, %(positionId)s, %(start)s, %(end)s, %(type)s)",
                            entity.__dict__)

            else:
                cur.execute("""
                    UPDATE designations.designation_
                    SET place_id = %(placeId)s, user_id = %(userId)s, position_id = %(positionId)s, dstart = %(start)s, dend = %(end)s
                    WHERE id = %(id)s
                """, entity.__dict__)


            return entity

        finally:
            cur.close()
