import uuid
from model.dao import SqlDAO
from model.users.entities.userPassword import UserPassword

class UserPasswordSqlDAO(SqlDAO):

    _schema = "credentials."
    _table = "user_password"

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





        @classmethod
        def findByIds(cls, ctx, ids, *args, **kwargs):
            assert ids is not None

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
                cur.execute(sql, (tuple(ids),tuple(condition["values"])))
                if cur.rowcount <= 0:
                    return []

                return [cls._fromResult(UserPassword(), o) for o in cur.fetchall()]

            finally:
                cur.close()
