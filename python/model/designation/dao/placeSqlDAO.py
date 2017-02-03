# -*- coding: utf-8 -*-
import uuid

from model.dao import SqlDAO
from model.designation.entities.place import Place



class PlaceSqlDAO(SqlDAO):

    _schema = "designations."
    _table = "place"
    _entity = Place

    @classmethod
    def _createSchema(cls, ctx):
        """ No asignar restriccion unique al atributo 'name' ya que puede eliminarse logicamente una oficina """
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



    @classmethod
    def persist(cls, ctx, entity):
        cur = ctx.con.cursor()
        try:
            if not hasattr(entity, 'id') or entity.id is None:
                entity.id = str(uuid.uuid4())
                cur.execute('insert into designations.place (id, name, type, parent, public) values (%(id)s, %(name)s, %(type)s, %(parent)s, %(public)s)', entity.__dict__)

            else:
                cur.execute('update designations.place set name = %(name)s, type = %(type)s, parent = %(parent)s, public = %(public)s where id = %(id)s', entity.__dict__)

            return entity
        finally:
            cur.close()
