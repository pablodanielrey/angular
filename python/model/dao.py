import logging

class DAO:

    dependencies = []
    _schema = None
    _table = None

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
    def findByFields(cls, con, cond = {}, ord = {}):
        condition = list()
        conditionValues = list()
        orderBy = list()

        #Definir condicion
        for k in cond:
            if cond[k] == "NOT NULL":
                condition.append("(" + k + " IS NOT NULL)")
            elif cond[k] == "NULL":
                condition.append("(" + k + " IS NULL)")
            else:
                condition.append("(" + k + " IN %s)")
                conditionValues.append(tuple(cond[k]))

        #Definir ordenamiento
        for k in ord:
            orderBy.append(k + " " + ord[k])


        sql = "SELECT * FROM " + cls._schema + cls._table

        if len(condition):
            sql = sql + " WHERE "
            sql = sql + ' AND ' .join(condition)

        if len(orderBy):
            sql = sql + " ORDER BY "
            sql = sql + ', ' .join(orderBy)

        sql = sql + "; "

        cur = con.cursor()
        cur.execute(sql, tuple(conditionValues))

        return [d['id'] for d in cur]



    @classmethod
    def findByIds(cls, con, ids):
        assert ids is not None

        if len(ids) <= 0:
            return []

        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM ' + cls._schema + cls._table + ' WHERE id IN %s', (tuple(ids),))
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
