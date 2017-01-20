import logging
from model import DAO, SqlContext
import re
import uuid



class SqlDAO(DAO):

    dependencies = []

    _schema = None
    _table = None
    _entity = None
    _mappings = None

    @classmethod
    def _select(cls, ctx):
        return isinstance(ctx, SqlContext)

    @classmethod
    def _condition(cls, **kwargs):
        condition = kwargs
        if "orderBy" in kwargs:
            del condition["orderBy"]

        conditionList = list()
        conditionValues = list()
        for k in condition:
            if type(condition[k]) == bool:
                cond = "({} IS NOT NULL)" if condition[k] else "({} IS NULL)"
                conditionList.append(cond.format(cls.namemapping(k)))
            else:
                if isinstance(condition[k], list):
                    if len(condition[k]) <= 0:
                        conditionList.append("(false)")
                    else:
                    conditionList.append("({} IN %s)".format(cls.namemapping(k)))
                    conditionValues.append(tuple(condition[k]))
                else:
                    conditionList.append('({} = %s)'.format(cls.namemapping(k)))
                    conditionValues.append(condition[k])

        return {"list":conditionList, "values":conditionValues}

    @classmethod
    def _orderBy(cls, **kwargs):
        orderBy = kwargs["orderBy"] if "orderBy" in kwargs else {}

        orderByList = list()

        for k in orderBy:
            orderByType = "ASC" if orderBy[k] else "DESC"
            orderByList.append("{} {}".format(cls.namemapping(k), orderByType))

        return orderByList

    @classmethod
    def namemapping(cls, name):
        name = cls._mappings[name] if cls._mappings is not None and name in cls._mappings else name
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


    @classmethod
    def _createSchema(cls, ctx):

        for dep in cls.dependencies:
            dep._createSchema(ctx)


    @classmethod
    def findById(cls, con, id):
        assert id is not None
        res = cls.findByIds(con, [id])
        return res[0] if len(res) else None

    @classmethod
    def findByIds(cls, ctx, ids, *args, **kwargs):
        orderBy = cls._orderBy(**kwargs)
        o = " ORDER BY {}".format(', ' .join(orderBy)) if len(orderBy) else ""
        sql = "SELECT * FROM {}{} WHERE id IN %s {};".format(cls._schema, cls._table, o)

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
        sql = "SELECT id FROM {}{}{}{};".format(cls._schema, cls._table, c, o)

        cur = ctx.con.cursor()
        try:
            cur.execute(sql, tuple(condition["values"]))
            if cur.rowcount <= 0:
                return []

            return [r['id'] for r in cur]

        finally:
            cur.close()


    @classmethod
    def deleteByIds(cls, ctx, ids, *args, **kwargs):
        ''' eliminar entidades  '''
        assert ids is not None
        assert isinstance(ids, list)

        cur = ctx.con.cursor()
        try:
            sql = 'delete from {}{} where id in %s'.format(cls._schema, cls._table)
            cur.execute(sql, (tuple(ids),))
        finally:
            cur.close()
