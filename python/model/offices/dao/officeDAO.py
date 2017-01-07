
from model.dao import SqlDAO
from model.offices.office import OfficeDAO

class OfficeSqlDAO(OfficeDAO, SqlDAO):

    _schema = "offices."
    _table  = "offices"

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS offices;

                CREATE TABLE IF NOT EXISTS offices.offices (
                  id VARCHAR NOT NULL PRIMARY KEY,
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

    @staticmethod
    def _fromResult(r):
        o = Office()
        o.id = r['id']
        o.name = r['name']
        o.telephone = r['telephone']
        o.number = r['nro']
        #o.type = r['type']
        o.type = None if r['type'] is None else [t for t in Office.officeType if t['value'] == r['type']][0]
        o.email = r['email']
        o.parent = r['parent']
        o.public = r['public']
        return o

    @classmethod
    def findChilds(cls, con, oid, types=None, tree=False):
        cids = set()
        pids = set()
        pids.add(oid)

        cur = con.cursor()
        try:
            while (len(pids) > 0):
                pid = pids.pop()
                cur.execute('select id from offices.offices where parent = %s and removed is null', (pid,))
                currentIds = [o['id'] for o in cur if o['id'] not in cids]
                if not tree:
                    cids.update(currentIds)
                else:
                    ''' evito loops '''
                    pids.update(set(currentIds) - cids)
                    cids.update(currentIds)

            if types is not None and len(cids) > 0:
                ''' de todos los hijos se seleccionan los de determinados tipos '''
                cur.execute('select id from offices.offices where id in %s and type in %s', (tuple(cids), tuple(types)))
                return [o['id'] for o in cur]
            else:
                return list(cids)

        finally:
            cur.close()

    @classmethod
    def findAll(cls, con, types=None):
        cur = con.cursor()
        try:
            if types is None:
                cur.execute('select id from offices.offices where removed is null')
                return [o['id'] for o in cur]
            else:
                assert isinstance(types, list)
                t = [o['value'] for o in types]
                cur.execute('select id from offices.offices where removed is null and type in %s',(tuple(t),))
                return [o['id'] for o in cur]

        finally:
            cur.close()

    @classmethod
    def persist(cls, con, office):
        ''' inserta o actualiza una oficia '''
        cur = con.cursor()
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
    def remove(cls, con, id):
        cur = con.cursor()
        try:
            cur.execute('update offices.offices set removed = NOW() where id = %s', (id,))
            return id
        finally:
            cur.close()
