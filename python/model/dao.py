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
    def findByIds(cls, con, ids):
        assert ids is not None
        if len(ids) <= 0:
            return []

        #Definir ordenamiento
        orderBy = list()
        for k in ord:
            orderBy.append(k + " " + ord[k])

        sql = 'SELECT * FROM ' + cls._schema + cls._table + ' WHERE id IN %s'

        if len(orderBy):
            sql = sql + " ORDER BY "
            sql = sql + ', ' .join(orderBy)

        sql = sql + "; "


        cur = con.cursor()
        try:
            cur.execute(sql, (tuple(ids),))
            if cur.rowcount <= 0:
                return []

            return [cls._fromResult(o) for o in cur.fetchall()]

        finally:
            cur.close()


    @classmethod
    def findById(cls, con, id):
        assert id is not None
        res = cls.findByIds(con, [id])
        return res[0] if len(res) else None


    @classmethod
    def findBy(cls, ctx, *args, **kwargs):
        condition = kwargs

        orderBy = {}
        if "orderBy" in kwargs:
            orderBy = kwargs["orderBy"]
            del condition["orderBy"]

        conditionList = list()
        conditionValues = list()
        orderByList = list()

        #Definir condicion
        for k in condition:
            if type(condition[k]) == bool:
                cond = "({} IS NOT NULL)" if condition[k] else "({} IS NULL)"
                conditionList.append(cond.format(cls.decamelize(k)))
            else:
                conditionList.append("({} IN %s)".format(cls.decamelize(k)))
                conditionValues.append(tuple(condition[k]))

        #Definir ordenamiento
        for k in orderBy:
            orderByType = "ASC" if orderBy[k] else "DESC"
            orderByList.append("{} {}".format(cls.decamelize(k), orderByType))

        if len(conditionList) and len(orderByList):
            c = ' AND ' .join(conditionList)
            o = ', ' .join(orderByList)
            sql = "SELECT * FROM {}{} WHERE {} ORDER BY {}".format(cls._schema, cls._table, c, o)
        elif len(conditionList) and not len(orderByList):
            c = ' AND ' .join(conditionList)
            sql = "SELECT * FROM {}{} WHERE {};".format(cls._schema, cls._table, c)

        elif not len(conditionList) and len(orderByList):
            o = ', ' .join(orderByList)
            sql = "SELECT * FROM {}{} ORDER BY {};".format(cls._schema, cls._table, o)

        else:
            sql = "SELECT * FROM {}{};".format(cls._schema, cls._table)

        print(sql)
        print(conditionValues)
        """
        cur = con.cursor()
        cur.execute(sql, tuple(conditionValues))

        return [d['id'] for d in cur]
        """
