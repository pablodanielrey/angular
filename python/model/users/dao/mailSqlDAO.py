import uuid
from model.dao import SqlDAO
from model.users.entities.mail import Mail

class MailSqlDAO(SqlDAO):

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)
        cur = ctx.con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS profile;

              CREATE TABLE IF NOT EXISTS profile.mails(
                id VARCHAR NOT NULL PRIMARY KEY,
                user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                email VARCHAR NOT NULL,
                confirmed boolean NOT NULL DEFAULT false,
                hash VARCHAR,
                created TIMESTAMP DEFAULT now()
              );
            """

            cur.execute(sql)

        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, m, r):
        m.id = r['id']
        m.userId = r['user_id']
        m.email = r['email']
        m.confirmed = r['confirmed']
        m.hash = r['hash']
        m.created = r['created']
        return m

    @classmethod
    def findByIds(cls, ctx, ids):
        ''' Obtiene el email identificado por el id '''
        assert isinstance(ids, list)
        cur = ctx.con.cursor()
        try:
            cur.execute('select * from profile.mails where id = %s', (eid,))
            return [cls._fromResult(Mail(), c) for c in cur]

        finally:
            cur.close()

    @classmethod
    def findByUserId(cls, ctx, userId):
        cur = ctx.con.cursor()
        try:
            cur.execute('select id from profile.mails where user_id = %s', (userId,))
            return [c['id'] for c in cur]

        finally:
            cur.close()


    @classmethod
    def persist(cls, ctx, mail):
        ''' crea o actualiza un email de usuario '''
        cur = ctx.con.cursor()
        try:
            if not hasattr(mail, 'id') or mail.id is None:
                mail.id = str(uuid.uuid4())
                params = mail.__dict__
                cur.execute('insert into profile.mails (id, user_id, email, confirmed, hash) values (%(id)s, %(userId)s, %(email)s, %(confirmed)s, %(hash)s)', params)
            else:
                params = mail.__dict__
                cur.execute('update profile.mails set user_id = %(userId)s, email = %(email)s, confirmed = %(confirmed)s, hash = %(hash)s where id = %(id)s', params)

            return mail.id

        finally:
            cur.close()

    @classmethod
    def delete(cls, ctx, mid):
        ''' Elimina el email dado por el id '''
        cur = ctx.con.cursor()
        try:
            cur.execute('delete from profile.mails where id = %s', (mid,))

        finally:
            cur.close()
