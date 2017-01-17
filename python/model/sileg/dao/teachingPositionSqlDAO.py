import uuid

from model.dao import SqlDAO
from model.designation.dao.positionSqlDAO import PositionSqlDAO
from model.sileg.entities.teachingPosition import TeachingPosition


class TeachingPositionSqlDAO(SqlDAO):

    dependencies = [PlaceSqlDAO]

    _schema = "sileg."
    _table  = "place"
    _entity = TeachingPosition

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)

        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS sileg;

                CREATE TABLE IF NOT EXISTS sileg.position (
                  id VARCHAR NOT NULL PRIMARY KEY REFERENCES designations.position (id),
                  detail VARCHAR,
                );

            """)
        finally:
            cur.close()


    @classmethod
    def _condition(cls, **kwargs):
        condition = kwargs
        if "orderBy" in kwargs:
            del condition["orderBy"]

        conditionList = list()
        conditionValues = list()
        for k in condition:
            if type(condition[k]) == bool:
                if k in ["detail"]:
                  cond = "(sileg.position.{} IS NOT NULL)" if condition[k] else "(sileg.position.{} IS NULL)"
                else:
                  cond = "(designations.position.{} IS NOT NULL)" if condition[k] else "(designations.position.{} IS NULL)"

                conditionList.append(cond.format(cls.namemapping(k)))
            else:
                if k in ["detail"]:
                    conditionList.append("(sileg.position.{} IN %s)".format(cls.namemapping(k)))
                else:
                    conditionList.append("(designations.position.{} IN %s)".format(cls.namemapping(k)))

                conditionValues.append(tuple(condition[k]))

        return {"list":conditionList, "values":conditionValues}



    @classmethod
    def _orderBy(cls, **kwargs):
        orderBy = kwargs["orderBy"] if "orderBy" in kwargs else {}

        orderByList = list()

        for k in orderBy:
            orderByType = "ASC" if orderBy[k] else "DESC"
            if k in ["detail"]:
                orderByList.append("sileg.position.{} {}".format(cls.namemapping(k), orderByType))
            else:
                orderByList.append("designations.position.{} {}".format(cls.namemapping(k), orderByType))

        return orderByList




    @classmethod
    def _fromResult(cls, entity, r):
        super()._fromResult(entity, r)
        entity.detail = r['detail']
        return o


    @classmethod
    def findByIds(cls, ctx, ids, *args, **kwargs):
        orderBy = cls._orderBy(**kwargs)
        o = " ORDER BY {}".format(', ' .join(orderBy)) if len(orderBy) else ""
        sql = """
            SELECT *
            FROM sileg.position
            INNER JOIN designations.position ON (sileg.position.id = designations.position.id)
            WHERE sileg.position.id IN %s
            {}
        """.format(o)

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
            SELECT sileg.position.id
            FROM sileg.position
            INNER JOIN designations.position ON (sileg.position.id = designations.position.id)
            {}{}
        """.format(c, o)

        cur = ctx.con.cursor()
        try:
            cur.execute(sql, tuple(condition["values"]))
            if cur.rowcount <= 0:
                return []

            return [r['id'] for r in cur]

        finally:
            cur.close()





    @classmethod
    def persist(cls, ctx, entity):
        ''' inserta o actualiza una oficia '''
        cur = ctx.con.cursor()
        try:
            if entity.id is None:
                entity.id = str(uuid.uuid4())
                params = entity.__dict__
                cur.execute('insert into designations.position (id, position, type) values (%(id)s, %(position)s, %(type)s)', params)
                cur.execute('insert into sileg.position (id, detail) values (%(id)s, %(detail)s)', params)

            else:
                params = entity.__dict__
                cur.execute('update designations.position set position = %(position)s, type = %(type)s where id = %(id)s', params)
                cur.execute('update sileg.position set position = %(position)s, type = %(type)s where id = %(id)s', params)

            return office

        finally:
            cur.close()
