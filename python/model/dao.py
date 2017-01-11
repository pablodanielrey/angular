import logging
from model import DAO, SqlContext
import re



class SqlDAO(DAO):

    dependencies = []
    _schema = None
    _table = None

    @classmethod
    def _select(cls, ctx):
        return isinstance(ctx, SqlContext)

    @staticmethod
    def _condition(**kwargs):
        condition = kwargs
        if "orderBy" in kwargs:
            del condition["orderBy"]

        conditionList = list()
        conditionValues = list()
        for k in condition:
            if type(condition[k]) == bool:
                cond = "({} IS NOT NULL)" if condition[k] else "({} IS NULL)"
                conditionList.append(cond.format(SqlDAO.decamelize(k)))
            else:
                conditionList.append("({} IN %s)".format(SqlDAO.decamelize(k)))
                conditionValues.append(tuple(condition[k]))

        return {"list":conditionList, "values":conditionValues}

    @staticmethod
    def _orderBy(**kwargs):
        orderBy = kwargs["orderBy"] if "orderBy" in kwargs else {}

        orderByList = list()

        for k in orderBy:
            orderByType = "ASC" if orderBy[k] else "DESC"
            orderByList.append("{} {}".format(SqlDAO.decamelize(k), orderByType))

        return orderByList


    @staticmethod
    def decamelize(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


    @classmethod
    def _createSchema(cls, con):
        for dep in cls._getDependencies():
            logging.debug('creando schema : {}'.format(dep.__name__))
            dep._createSchema(con)

        for c in cls.__subclasses__():
            logging.debug('creando schema : {}'.format(c.__name__))
            c._createSchema(con)

    @classmethod
    def _getDependencies(cls):
        return cls.dependencies

    @classmethod
    def findById(cls, con, id):
        assert id is not None
        res = cls.findByIds(con, [id])
        return res[0] if len(res) else None

    @classmethod
    def find(cls, ctx, *args, **kwargs):
        condition = cls._condition(**kwargs)
        orderBy = cls._orderBy(**kwargs);

        if len(condition["list"]) and len(orderBy):
            c = ' AND ' .join(condition["list"])
            o = ', ' .join(orderBy)
            sql = "SELECT id FROM {}{} WHERE {} ORDER BY {}".format(cls._schema, cls._table, c, o)

        elif len(condition["list"]) and not len(orderBy):
            c = ' AND ' .join(condition["list"])
            sql = "SELECT id FROM {}{} WHERE {};".format(cls._schema, cls._table, c)

        elif not len(condition["list"]) and len(orderBy):
            o = ', ' .join(orderBy)
            sql = "SELECT id FROM {}{} ORDER BY {};".format(cls._schema, cls._table, o)

        else:
            sql = "SELECT id FROM {}{};".format(cls._schema, cls._table)

        cur = ctx.con.cursor()
        try:
            cur.execute(sql, tuple(condition["values"]))
            if cur.rowcount <= 0:
                return []

            return [r['id'] for r in cur]

        finally:
            cur.close()
