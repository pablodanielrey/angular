import uuid
from model.dao import SqlDAO
from model.users.entities.userPassword import UserPassword

class UserPasswordSqlDAO(SqlDAO):

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)
        cur = ctx.con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS credentials;

              CREATE TABLE IF NOT EXISTS credentials.user_password(
                id VARCHAR NOT NULL PRIMARY KEY,
                user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                username VARCHAR NOT NULL UNIQUE,
                password VARCHAR NOT NULL,
                updated TIMESTAMP DEFAULT now()
              );
            """
            cur.execute(sql)

        finally:
            cur.close()


    @classmethod
    def _fromResult(cls, up, r):
        up.id = r['id']
        up.userId = r['user_id']
        up.username = r['username']
        up.password = r['password']
        up.updated = r['updated']
        return up

    @classmethod
    def findByIds(cls, ctx, ids):
        assert isinstance(ids, list)
        cur = ctx.con.cursor()
        try:
            cur.execute('select * from credentials.user_password where id in %s', (tuple(ids),))
            if cur.rowcount <= 0:
                return []
            data = [cls._fromResult(UserPassword(), c) for c in cur]
            return data

        finally:
            cur.close()

    @classmethod
    def findByUserPassword(cls, ctx, username, password):
        cur = ctx.con.cursor()
        try:
            cur.execute('select id from credentials.user_password where username = %s and password = %s', (username, password))
            return [c['id'] for c in cur]

        finally:
            cur.close()

    @classmethod
    def findByUsername(cls, ctx, username):
        cur = ctx.con.cursor()
        try:
            cur.execute('select id from credentials.user_password where username = %s', (username,))
            return [c['id'] for c in cur]

        finally:
            cur.close()

    @classmethod
    def findByUserId(cls, ctx, userId):
        cur = ctx.con.cursor()
        try:
            cur.execute('select id from credentials.user_password where user_id = %s', (userId,))
            return [c['id'] for c in cur]

        finally:
            cur.close()

    @classmethod
    def persist(cls, ctx, up):
        cur = ctx.con.cursor()
        try:
            if not hasattr(up, 'id') or up.id is None:
                up.id = str(uuid.uuid4())
                params = up.__dict__
                cur.execute('insert into credentials.user_password (id, user_id, username, password, updated) values (%(id)s, %(userId)s, %(username)s, %(password)s, now())', params)
            else:
                params = up.__dict__
                cur.execute('update credentials.user_password set user_id = %(userId)s, username = %(username)s, password = %(password)s, updated = now() where id = %(id)s', params)

            return up.id

        finally:
            cur.close()
