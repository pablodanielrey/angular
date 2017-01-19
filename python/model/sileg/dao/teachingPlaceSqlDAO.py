import uuid

from model.dao import SqlDAO
from model.designation.dao.placeSqlDAO import PlaceSqlDAO
from model.sileg.entities.teachingPlace import TeachingPlace


class TeachingPlaceSqlDAO(PlaceSqlDAO):


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

                CREATE TABLE IF NOT EXISTS sileg.place_ (
                  id VARCHAR NOT NULL PRIMARY KEY REFERENCES designations.place (id),
                  telephone VARCHAR,
                  email VARCHAR
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
                if k in ["telephone", "email"]:
                  cond = "(sileg.place_.{} IS NOT NULL)" if condition[k] else "(sileg.place_.{} IS NULL)"
                else:
                  cond = "(designations.place.{} IS NOT NULL)" if condition[k] else "(designations.place.{} IS NULL)"

                conditionList.append(cond.format(cls.namemapping(k)))
            else:
                if k in ["telephone", "email"]:
                    conditionList.append("(sileg.place_.{} IN %s)".format(cls.namemapping(k)))
                else:
                    conditionList.append("(designations.place.{} IN %s)".format(cls.namemapping(k)))

                conditionValues.append(tuple(condition[k]))

        return {"list":conditionList, "values":conditionValues}



    @classmethod
    def _orderBy(cls, **kwargs):
        orderBy = kwargs["orderBy"] if "orderBy" in kwargs else {}

        orderByList = list()

        for k in orderBy:
            orderByType = "ASC" if orderBy[k] else "DESC"
            if k in ["telephone", "email"]:
                orderByList.append("sileg.place_.{} {}".format(cls.namemapping(k), orderByType))
            else:
                orderByList.append("designations.place.{} {}".format(cls.namemapping(k), orderByType))

        return orderByList




    @classmethod
    def _fromResult(cls, o, r):
        super()._fromResult(o, r)
        o.telephone = r['telephone']
        o.email = r['email']
        return o


    @classmethod
    def findByIds(cls, ctx, ids, *args, **kwargs):
        orderBy = cls._orderBy(**kwargs)
        o = " ORDER BY {}".format(', ' .join(orderBy)) if len(orderBy) else ""
        sql = """
            SELECT *
            FROM sileg.place_
            INNER JOIN designations.place ON (sileg.place_.id = designations.place.id)
            WHERE sileg.place_.id IN %s
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
            SELECT sileg.place_.id
            FROM sileg.place_
            INNER JOIN designations.place ON (sileg.place_.id = designations.place.id)
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
        hasId = hasattr(entity, 'id') and entity.id is not None
        super().persist(ctx, entity)

        cur = ctx.con.cursor()
        try:
            if not hasId:
                cur.execute('insert into sileg.place_ (id, telephone, email) values (%(id)s, %(telephone)s, %(email)s)', entity.__dict__)

            else:
                cur.execute('update sileg.place_ set telephone = %(telephone)s, email = %(email)s, where id = %(id)s', entity.__dict__)

            return entity

        finally:
            cur.close()
