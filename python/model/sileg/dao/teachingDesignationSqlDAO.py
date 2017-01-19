# -*- coding: utf-8 -*-
import uuid

from model.sileg.entities.teachingDesignation import TeachingDesignation
from model.designation.dao.designationSqlDAO import DesignationSqlDAO
from model.sileg.dao.teachingPlaceSqlDAO import TeachingPlaceSqlDAO
from model.sileg.dao.teachingPositionSqlDAO import TeachingPositionSqlDAO


class TeachingDesignationSqlDAO(DesignationSqlDAO):
    ''' DAO teachingDesignation '''

    dependencies = [TeachingPlaceSqlDAO, TeachingPositionSqlDAO]
    _schema = "sileg."
    _table = "designation_"
    _entity = TeachingDesignation
    _mappings = {
        'out':'dout'
    }

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)
        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS sileg;

                CREATE TABLE IF NOT EXISTS sileg.designation_ (
                    id VARCHAR PRIMARY KEY NOT NULL REFERENCES designations.designation_ (id),

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
            cur.execute('update sileg.designation_ set dout = NOW() where id in %s', (tuple(ids),))
        finally:
            cur.close()



    @classmethod
    def persist(cls, ctx, entity):
        hasId = hasattr(entity, 'id') and entity.id is not None
        super().persist(ctx, entity)

        ''' inserta o actualiza una oficia '''
        cur = ctx.con.cursor()
        try:
            if not hasId:
                cur.execute("""
                    INSERT INTO sileg.designation_ (id, dout, resolution, record)
                    VALUES (%(id)s, %(out)s, %(resolution)s, %(record)s);
                """, entity.__dict__)

            else:
                cur.execute("""
                    UPDATE sileg.designation_
                    SET dout = %(out)s, resolution = %(resolution)s, record = %(record)s
                    WHERE id = %(id)s
                """, entity.__dict__)

            return entity

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
                  cond = "(sileg.designation_.{} IS NOT NULL)" if condition[k] else "(sileg.designation_.{} IS NULL)"
                else:
                  cond = "(designations.designation_.{} IS NOT NULL)" if condition[k] else "(designations.designation_.{} IS NULL)"

                conditionList.append(cond.format(cls.namemapping(k)))
            else:
                if k in ["out", "resolution", "record"]:
                    conditionList.append("(sileg.designation_.{} IN %s)".format(cls.namemapping(k)))
                else:
                    conditionList.append("(designations.designation_.{} IN %s)".format(cls.namemapping(k)))

                conditionValues.append(tuple(condition[k]))

        return {"list":conditionList, "values":conditionValues}



    @classmethod
    def _orderBy(cls, **kwargs):
        orderBy = kwargs["orderBy"] if "orderBy" in kwargs else {}

        orderByList = list()

        for k in orderBy:
            orderByType = "ASC" if orderBy[k] else "DESC"
            if k in ["out", "resolution", "record"]:
                orderByList.append("sileg.designation_.{} {}".format(cls.namemapping(k), orderByType))
            else:
                orderByList.append("designations.designation_.{} {}".format(cls.namemapping(k), orderByType))

        return orderByList




    @classmethod
    def findByIds(cls, ctx, ids, *args, **kwargs):
        orderBy = cls._orderBy(**kwargs)
        o = " ORDER BY {}".format(', ' .join(orderBy)) if len(orderBy) else ""
        sql = """
            SELECT *
            FROM sileg.designation_
            INNER JOIN designations.designation_ ON (sileg.designation_.id = designations.designation_.id)
            WHERE sileg.designation_.id IN %s
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
            SELECT sileg.designation_.id
            FROM sileg.designation_
            INNER JOIN designations.designation_ ON (sileg.designation_.id = designations.designation_.id)
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
