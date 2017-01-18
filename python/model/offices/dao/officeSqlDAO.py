import uuid

from model.dao import SqlDAO
from model.offices.entities.office import Office
from model.designation.dao.placeSqlDAO import PlaceSqlDAO
from model.designation.entities.designation import Designation

class OfficeSqlDAO(PlaceSqlDAO):

    _schema = "offices."
    _table  = "office"
    _mappings = {"number":"nro"}
    _entity = Office


    @classmethod
    def _condition(cls, **kwargs):
        condition = kwargs
        if "orderBy" in kwargs:
            del condition["orderBy"]

        conditionList = list()
        conditionValues = list()
        for k in condition:
            if type(condition[k]) == bool:
                if k in ["telephone", "number", "email"]:
                  cond = "({} IS NOT NULL)" if condition[k] else "({} IS NULL)"
                else:
                  cond = "(designations.place.{} IS NOT NULL)" if condition[k] else "(designations.place.{} IS NULL)"

                conditionList.append(cond.format(cls._schema, cls._table, cls.namemapping(k)))
            else:
                if k in ["telephone", "number", "email"]:
                    conditionList.append("({} IN %s)".format(cls.namemapping(k)))
                else:
                    conditionList.append("((designations.place.{} IN %s)".format(cls.namemapping(k)))

                conditionValues.append(tuple(condition[k]))

        return {"list":conditionList, "values":conditionValues}



    @classmethod
    def _orderBy(cls, **kwargs):
        orderBy = kwargs["orderBy"] if "orderBy" in kwargs else {}

        orderByList = list()

        for k in orderBy:
            orderByType = "ASC" if orderBy[k] else "DESC"
            if k in ["telephone", "number", "email"]:
                orderByList.append("{}{}.{} {}".format(cls._schema, cls._table, cls.namemapping(k), orderByType))
            else:
                orderByList.append("{}{}.{} {}".format(super()._schema, super()._table, cls.namemapping(k), orderByType))

        return orderByList



    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)

        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS offices;

                CREATE TABLE IF NOT EXISTS offices.office (
                  id VARCHAR NOT NULL PRIMARY KEY REFERENCES designations.place (id),
                  telephone VARCHAR,
                  nro VARCHAR,
                  email VARCHAR
                );
            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, o, r):
        super()._fromResult(o, r)
        o.telephone = r['telephone']
        o.number = r['nro']
        o.email = r['email']
        return o


    @classmethod
    def findByIds(cls, ctx, ids, *args, **kwargs):
        orderBy = cls._orderBy(**kwargs)
        o = " ORDER BY {}".format(', ' .join(orderBy)) if len(orderBy) else ""
        sql = """
            SELECT *
            FROM offices.office
            INNER JOIN designations.place ON (offices.office.id = designations.place.id)
            WHERE offices.office.id IN %s
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
            SELECT offices.office.id
            FROM offices.office
            INNER JOIN designations.place ON (offices.office.id = designations.place.id)
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
    def findByUserId(cls, ctx, usersId, tree=False, *args, **kwargs):
        """
        Buscar oficinas por usuario
        Parameters:
          usersIds (lista) - lista de usuarios a consutlar.
          tree (bool) - flag para indicar si se deben buscar hijos
        """
        designations = Designation.find(ctx, userId=[userId], positionId=[1]).fetch(ctx)
        ids = [d.officeId for d in designations]

        if tree:
            ids.extend(cls.findChildsByIds(ctx, ids, False))

        if(kwargs):
            idsAux = cls.find(ctx, *args, **kwargs)
            ids = list(set(ids) & set(idsAux))

        return list(set(ids))


    @classmethod
    def findChildsByIds(cls, ctx, officeIds, tree=False, *args, **kwargs):
        childIds = cls.find(ctx, parent=officeIds, *args, **kwargs)

        if(tree):
            officeIdsAux = list(set(childIds) - set(officeIds))
            childIdsAux = cls.findChildsByIds(ctx, officeIdsAux, False, *args, **kwargs)
            childIds.extend(childIdsAux)

        return list(set(childIds))


    @classmethod
    def persist(cls, ctx, office):
        hasId = 'id' in office or office.id is not None
        super().persist(ctx, office)

        ''' inserta o actualiza una oficia '''
        cur = ctx.con.cursor()
        try:
            if not hasId:
                #office.id = str(uuid.uuid4())
                params = office.__dict__
                #cur.execute('insert into designations.place (id, name, type, parent, public) values (%(id)s, %(name)s, %(type)s, %(parent)s, %(public)s)', params)
                cur.execute('insert into offices.office (id, telephone, nro, email) values (%(id)s, %(telephone)s, %(number)s, %(email)s)', params)

            else:
                params = office.__dict__
                #cur.execute('update designations.place set name = %(name)s, type = %(type)s, parent = %(parent)s, public = %(public)s where id = %(id)s', params)
                cur.execute('update offices.office set telephone = %(telephone)s, nro = %(number)s, email = %(email)s, where id = %(id)s', params)

            return office

        finally:
            cur.close()
