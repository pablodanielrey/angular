import copy
import uuid

from model.dao import SqlDAO
from model.oauth.entities.oauth1 import AccessToken

class AccessTokenSqlDAO(SqlDAO):

    _schema = 'oauth.'
    _table = 'access_token'
    _entity = AccessToken

    @classmethod
    def _createSchema(cls, ctx):
        cur = ctx.con.cursor()
        try:
            cur.execute("create schema if not exists {}".format(cls._schema.replace('.','')))
            cur.execute("""create table if not exists {}{} (
                             id varchar primary key default uuid_generate_v4(),
                             client_id varchar,
                             user_id varchar,
                             token varchar,
                             secret varchar,
                             scopes varchar,
                             created timestamptz default NOW()
                            )""".format(cls._schema, cls._table))
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, c, r):
        c.id = r['id']
        c.clientId = r['client_id']
        c.userId = ['user_id']
        c.token = r['token']
        c.secret = r['secret']
        c.scopes = r['scopes'].split()
        return c

    @classmethod
    def persist(cls, ctx, c):
        cur = ctx.con.cursor()
        try:
            if not hasattr(c, 'id') or c.id is None:
                c.id = str(uuid.uuid4())
                p = copy.copy(c)
                p.scopes_transformed = ' '.join(p.scopes)
                cur.execute("insert into {}{} (id, client_id, user_id, token, secret, scopes) "
                            "values (%(id)s, %(clientId)s, %(userId)s, %(token)s, %(secret)s, %(scopes_transformed)s)"
                            .format(cls._schema, cls._table),
                            p.__dict__)
            else:
                p = copy.copy(c)
                p.scopes_transformed = ' '.join(p.scopes)
                cur.execute("update {}{} set (client_id = %(clientId)s, "
                                             "user_id = %(userId)s, "
                                             "token = %(token)s, "
                                             "secret = %(secret)s, "
                                             "scopes = %(scopes_transformed)s "
                                             "where id = %(id)s"
                            .format(cls._schema, cls._table),
                            p.__dict__)
            return c
        finally:
            cur.close()
