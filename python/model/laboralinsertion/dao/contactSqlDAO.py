from model.dao import SqlDAO
from model.laboralinsertion.entities.contact import Contact

class ContactSqlDAO(SqlDAO):

    _schema = "laboral_insertion."
    _table = "contacts"
    _entity = Contact

    @classmethod
    def _createSchema(cls, con):
        super().createSchema(con)

        cur = con.cursor()
        try:
            cur.execute("""
                create table laboral_insertion.contacts (
                    id varchar primary key,
                    name varchar,
                    email varchar,
                    telephone varchar,
                    company_id varchar not null references laboral_insertion.companies (id)
                )
            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, c, r):
        c.id = r['id']
        c.name = r['name']
        c.email = r['email']
        c.telephone = r['telephone']
        c.companyId = r['company_id']
        return c

    @classmethod
    def persist(cls, ctx, contact):
        if contact is None:
            return

        cur = ctx.con.cursor()
        try:
            contact.id = str(uuid.uuid4())
            ins = contact.__dict__
            cur.execute('insert into laboral_insertion.contacts (id, name, email, telephone, company_id) values  '
                        '(%(id)s, %(name)s, %(email)s, %(telephone)s, %(companyId)s)', ins)

        finally:
            cur.close()
