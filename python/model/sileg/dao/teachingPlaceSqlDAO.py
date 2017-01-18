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

                CREATE TABLE IF NOT EXISTS sileg.place (
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
                  cond = "(sileg.place.{} IS NOT NULL)" if condition[k] else "(sileg.place.{} IS NULL)"
                else:
                  cond = "(designations.place.{} IS NOT NULL)" if condition[k] else "(designations.place.{} IS NULL)"

                conditionList.append(cond.format(cls.namemapping(k)))
            else:
                if k in ["telephone", "email"]:
                    conditionList.append("(sileg.place.{} IN %s)".format(cls.namemapping(k)))
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
                orderByList.append("sileg.place.{} {}".format(cls.namemapping(k), orderByType))
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
            FROM sileg.place
            INNER JOIN designations.place ON (sileg.place.id = designations.place.id)
            WHERE sileg.place.id IN %s
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
            SELECT sileg.place.id
            FROM sileg.place
            INNER JOIN designations.place ON (sileg.place.id = designations.place.id)
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
    def persist(cls, ctx, office):
        ''' inserta o actualiza una oficia '''
        cur = ctx.con.cursor()
        try:
            if office.id is None:
                office.id = str(uuid.uuid4())
                params = office.__dict__
                cur.execute('insert into designations.place (id, name, type, parent, public) values (%(id)s, %(name)s, %(type)s, %(parent)s, %(public)s)', params)
                cur.execute('insert into sileg.place (id, telephone, email) values (%(id)s, %(telephone)s, %(email)s)', params)

            else:
                params = office.__dict__
                cur.execute('update designations.place set name = %(name)s, type = %(type)s, parent = %(parent)s, public = %(public)s where id = %(id)s', params)
                cur.execute('update sileg.place set telephone = %(telephone)s, email = %(email)s, where id = %(id)s', params)

            return office

        finally:
            cur.close()
