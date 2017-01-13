from model.dao import SqlDAO
from model.offices.entities.office import Office
from model.designation.entities.designation import Designation

class OfficeSqlDAO(SqlDAO):

    _schema = "offices."
    _table  = "offices"
    _mappings = {"number":"nro"}
    _entity = Office

    @classmethod
    def _createSchema(cls, ctx):
        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS offices;

                CREATE TABLE IF NOT EXISTS offices.offices (
                id VARCHAR NOT NULL PRIMARY KEY REFERENCES designations.place (id),
                  name VARCHAR NOT NULL,
                  telephone VARCHAR,
                  nro VARCHAR,
                  email VARCHAR,
                  parent VARCHAR REFERENCES offices.offices (id),
                  type VARCHAR NOT NULL,
                  removed TIMESTAMPTZ,
                  public boolean default false,
                  UNIQUE (name)
                );

            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, o, r):
        o.id = r['id']
        o.name = r['name']
        o.telephone = r['telephone']
        o.number = r['nro']
        o.type = r['type']
        o.email = r['email']
        o.parent = r['parent']
        o.public = r['public']
        o.removed = r['removed']
        return o


    @classmethod
    def findByIds(cls, ctx, ids, *args, **kwargs):
        orderBy = cls._orderBy(**kwargs)
        o = " ORDER BY {}".format(', ' .join(orderBy)) if len(orderBy) else ""
        sql = """
            SELECT * FROM {}{}
            INNER JOIN designations.place p ON (o.id = p.id)
            WHERE id IN %s
            {}
        """.format(cls._schema, cls._table, o)

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
            SELECT id FROM {}{}
            INNER JOIN designations.place p ON (o.id = p.id)
            {}{}
        """.format(cls._schema, cls._table, c, o)

        cur = ctx.con.cursor()
        try:
            cur.execute(sql, tuple(condition["values"]))
            if cur.rowcount <= 0:
                return []

            return [r['id'] for r in cur]

        finally:
            cur.close()


    @classmethod
    def findByUserId(cls, ctx, usersIds, tree=False, *args, **kwargs):
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
        ''' inserta o actualiza una oficia '''
        cur = ctx.con.cursor()
        try:
            if office.id is None:
                office.id = str(uuid.uuid4())
                params = office.__dict__
                cur.execute('insert into offices.offices (id, name, telephone, nro, type, parent, email, public) values (%(id)s, %(name)s, %(telephone)s, %(number)s, %(type)s, %(parent)s, %(email)s, %(public)s)', params)
            else:
                params = office.__dict__
                cur.execute('update offices.offices set name = %(name)s, telephone = %(telephone)s, nro = %(number)s, type = %(type)s, parent = %(parent)s, email = %(email)s, public = %(public)s where id = %(id)s', params)

            return office.id

        finally:
            cur.close()



    @classmethod
    def deleteByIds(cls, ctx, ids):
        cur = ctx.con.cursor()
        try:
            cur.execute('update offices.offices set removed = NOW() where id in %s', (tuple(ids),))
            return ids
        finally:
            cur.close()
