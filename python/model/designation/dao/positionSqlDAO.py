# -*- coding: utf-8 -*-
from model.dao import SqlDAO
from model.designation.entities.position import Position


class PositionSqlDAO(SqlDAO):

    _schema = "designations."
    _table = "positions"
    _entity = Position

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)
        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS designations.position (
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

    @classmethod
    def insert(cls, ctx, entity):
        cur = ctx.con.cursor()
        try:
            cur.execute("""
                INSERT INTO designations.position (id, position, type)
                VALUES (%(id)s, %(position)s, %(type)s)
            """, entity.__dict__)

            return entity
        finally:
            cur.close()

    @classmethod
    def update(cls, ctx, entity):
        cur = ctx.con.cursor()
        try:
            cur.execute("""
                UPDATE designations.position
                SET position = %(position)s, type = %(type)s
                WHERE id = %(id)s;
            """, entity.__dict__)

            return entity
        finally:
            cur.close()
