# -*- coding: utf-8 -*-
from model.dao import SqlDAO
from model.designation.entities.position import Place


class PlaceSqlDAO(SqlDAO):

    _schema = "designations."
    _table = "place"
    _entity = Place

    @classmethod
    def _createSchema(cls, ctx):
        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS designations.place (
                    id VARCHAR NOT NULL PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    type VARCHAR NOT NULL,
                    parent VARCHAR REFERENCES offices.offices (id),
                    removed TIMESTAMPTZ,
                    public boolean default false,
                    UNIQUE (name)
                );
            """)
        finally:
            cur.close()


    @classmethod
    def _fromResult(cls, p, r):
        p.id = r['id']
        p.name = r['name']
        p.type = r['type']
        p.parent = r['parent']
        p.public = r['public']
        p.removed = r['removed']
        return p
