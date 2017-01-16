from model.dao import SqlDAO
from model.designation.dao.placeSqlDAO import PlaceSqlDAO
from model.sileg.entities.teachingPlace import TeachingPlace
from model.designation.entities.designation import Designation


class TeachingPlaceSqlDAO(SqlDAO):
    
    dependencies = [PlaceSqlDAO]

    _schema = "sileg."
    _table  = "place"
    _entity = TeachingPlace

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)

        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS sileg;

                CREATE TABLE IF NOT EXISTS sileg.place (
                  id VARCHAR NOT NULL PRIMARY KEY REFERENCES designations.place (id),
                  telephone VARCHAR,
                  email VARCHAR,
                );

            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, entity, result):
        entity.id = r['id']
        entity.name = r['name']
        entity.telephone = r['telephone']
        entity.type = r['type']
        entity.email = r['email']
        entity.parent = r['parent']
        entity.public = r['public']
        entity.removed = r['removed']
        return entity


    @classmethod
    def findByIds(cls, ctx, ids, *args, **kwargs):
        orderBy = cls._orderBy(**kwargs)
        o = " ORDER BY {}".format(', ' .join(orderBy)) if len(orderBy) else ""
        sql = """
            SELECT * FROM {}{}
            INNER JOIN designations.place p ON (o.id = p.id)
            WHERE id IN %s
            {}
        """.format(cls._schema, cls._table, o)

        cur = ctx.con.cursor()
        try:
            cur.execute(sql, (tuple(ids),))
            return [cls._fromResult(cls._entity(), c) for c in cur ]


        finally:
            cur.close()

    @classmethod
    def find(cls, ctx, *args, **kwargs):
        condition = cls._condition(**kwargs)
        orderBy = cls._orderBy(**kwargs);

        c = " WHERE {}".format(' AND ' .join(condition["list"])) if len(condition["list"]) else ""
        o = " ORDER BY {}".format(', ' .join(orderBy)) if len(orderBy) else ""
        sql = """
            SELECT id FROM {}{}
            INNER JOIN designations.place p ON (o.id = p.id)
            {}{}
        """.format(cls._schema, cls._table, c, o)

        cur = ctx.con.cursor()
        try:
            cur.execute(sql, tuple(condition["values"]))
            if cur.rowcount <= 0:
                return []

            return [r['id'] for r in cur]

        finally:
            cur.close()
