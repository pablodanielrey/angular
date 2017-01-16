# -*- coding: utf-8 -*-
from model.dao import SqlDAO
from model.designation.entities.place import Place



class PlaceSqlDAO(SqlDAO):

    _schema = "designations."
    _table = "place"
    _entity = Place

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)

        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS designations.place (
                    id VARCHAR NOT NULL PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    type VARCHAR NOT NULL,
                    parent VARCHAR REFERENCES designations.place (id),
                    removed TIMESTAMPTZ,
                    public boolean default false,
                    UNIQUE (name)
                );
            """)
            print(cur.statusmessage)
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




    @classmethod
    def deleteByIds(cls, ctx, ids):
        cur = ctx.con.cursor()
        try:
            cur.execute('update {}{} set removed = NOW() where id in %s'.format(PlaceSqlDAO._schema, PlaceSqlDAO._table), (tuple(ids),))
            return ids
        finally:
            cur.close()
