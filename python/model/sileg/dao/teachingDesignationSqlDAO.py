# -*- coding: utf-8 -*-
import uuid

from model.designation.dao.DesignationSqlDAO import DesignationSqlDAO
from model.sileg.entities.teachingDesignation import TeachingDesignation

class TeachingDesignationSqlDAO(DesignationSqlDAO):
    ''' DAO teachingDesignation '''

    _schema = "sileg."
    _table = "designation"
    _entity = TeachingDesignation
    _mappings = {
        'out':'dout'
    }

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(con)
        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS sileg.designation (
                    id VARCHAR PRIMARY KEY VARCHAR NOT NULL REFERENCES designations.designation (id),

                    dout DATE,
                    resolution VARCHAR,
                    record VARCHAR,

                    created timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, d, r):
        d = super()._fromResult(d, r)
        d.out = r["dout"]
        d.resolution = r["resolution"]
        d.record = r["record"]

        return d

    @classmethod
    def removeByIds(cls, ctx, ids):
        assert ids is not None
        assert isinstance(ids, list)
        cur = ctx.con.cursor()
        try:
            cur.execute('update sileg.designation set dout = NOW() where id in %s', (tuple(ids),))
        finally:
            cur.close()

    @classmethod
    def persist(cls, ctx, desig):
        cur = ctx.con.cursor()
        try:
            if not hasattr(desig, 'id'):
                desig.id = str(uuid.uuid4())

            cur.execute("""
              insert into designations.designation (id, office_id, user_id, position_id, dstart, dend)
              values (%(id)s, %(officeId)s, %(userId)s, %(positionId)s, %(start)s, %(end)s)
            """, desig.__dict__)

            cur.execute("""
              insert into sileg.designation (id, dout, resolution, record)
              values (%(id)s, %(dout)s, %(resolution)s, %(record)s)
            """, desig.__dict__)

            return desig
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
                    if k in ["out", "resolution", "record"]:
                      cond = "(sileg.designation.{} IS NOT NULL)" if condition[k] else "(sileg.place.{} IS NULL)"
                    else:
                      cond = "(designations.designation.{} IS NOT NULL)" if condition[k] else "(designations.place.{} IS NULL)"

                    conditionList.append(cond.format(cls.namemapping(k)))
                else:
                    if k in ["out", "resolution", "record"]:
                        conditionList.append("(sileg.designation.{} IN %s)".format(cls.namemapping(k)))
                    else:
                        conditionList.append("(designations.designation.{} IN %s)".format(cls.namemapping(k)))

                    conditionValues.append(tuple(condition[k]))

            return {"list":conditionList, "values":conditionValues}



        @classmethod
        def _orderBy(cls, **kwargs):
            orderBy = kwargs["orderBy"] if "orderBy" in kwargs else {}

            orderByList = list()

            for k in orderBy:
                orderByType = "ASC" if orderBy[k] else "DESC"
                if k in ["out", "resolution", "record"]:
                    orderByList.append("sileg.designation.{} {}".format(cls.namemapping(k), orderByType))
                else:
                    orderByList.append("designations.designation.{} {}".format(cls.namemapping(k), orderByType))

            return orderByList




    @classmethod
    def findByIds(cls, ctx, ids, *args, **kwargs):
        orderBy = cls._orderBy(**kwargs)
        o = " ORDER BY {}".format(', ' .join(orderBy)) if len(orderBy) else ""
        sql = """
            SELECT *
            FROM sileg.designation
            INNER JOIN designations.designation ON (sileg.designation.id = designations.designation.id)
            WHERE sileg.designation.id IN %s
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
            SELECT sileg.designation.id
            FROM sileg.designation
            INNER JOIN designations.designation ON ({}{}.id = designations.designation.id)
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
