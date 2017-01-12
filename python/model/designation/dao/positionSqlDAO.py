# -*- coding: utf-8 -*-
from model.dao import SqlDAO
from model.designation.entities.position import Position


class PositionSqlDAO(SqlDAO):

    _schema = "designations."
    _table = "positions"
    _entity = Position

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS designations.positions (
                  id VARCHAR PRIMARY KEY,
                  position VARCHAR,
                  type INTEGER,
                  created TIMESTAMPTZ default now()
                );
            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, p, r):
        p.id = r['id']
        p.position = r['position']
        p.type = r['type']
        return p
