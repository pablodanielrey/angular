from model.dao import SqlDAO
from model.laboralinsertion.entities.company import Company
from model.laboralinsertion.entities.contact import Contact

class CompanySqlDAO(SqlDAO):

    _schema = "laboral_insertion."
    _table = "companies"
    _entity = Company



    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(con)

        cur = ctx.con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS laboral_insertion;

                create table IF NOT EXISTS laboral_insertion.companies (
                    id varchar primary key,
                    name varchar not null,
                    detail varchar,
                    cuit varchar not null,
                    teacher varchar,
                    manager varchar,
                    address varchar,
                    begincm timestamptz default now(),
                    endcm timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, c, r):
        ''' carga los datos desde el resultado pasad por parametro '''
        c.id = r["id"]
        c.name = r['name']
        c.detail = r['detail']
        c.cuit = r['cuit']
        c.teacher = r['teacher']
        c.manager = r['manager']
        c.address = r['address']
        c.beginCM = r['begincm']
        c.endCM = r['endcm']
        return c

    @classmethod
    def verifyData(cls, company):
        if not hasattr(company, 'address'):
            company.address = ''

    @classmethod
    def persist(cls, ctx, company):
        if company is None:
            return None

        cur = ctx.con.cursor()

        try:
            if not hasattr(company, 'id'):
                cls.verifyData(company)
                company.id = str(uuid.uuid4())
                ins = company.__dict__
                cur.execute('insert into laboral_insertion.companies (id, name, detail, cuit, teacher, manager, address, beginCM, endCM) values ('
                            '%(id)s, %(name)s, %(detail)s, %(cuit)s, %(teacher)s, %(manager)s, %(address)s, %(beginCM)s, %(endCM)s)', ins)
            else:
                params = company.__dict__
                cur.execute('update laboral_insertion.companies set name = %(name)s, detail = %(detail)s, cuit = %(cuit)s, teacher = %(teacher)s, '
                            'manager = %(manager)s, address = %(address)s, beginCM = %(beginCM)s, endCM = %(endCM)s where id = %(id)s', params)

                ctx.dao(Contact).deleteByCompany(ctx, company.id)

            for c in company.contacts:
                c.companyId = company.id
                ctx.dao(Contact).persist(ctx, c)

            return company.id

        finally:
            cur.close()
