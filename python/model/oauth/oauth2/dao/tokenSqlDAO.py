import copy
import uuid

from model.dao import SqlDAO
from model.oauth.oauth2.entities.oauth import BaseToken, AuthorizationToken, BearerToken

class BaseTokenSqlDAO(SqlDAO):

    _schema = 'oauth2.'
    _table = 'token'
    _entity = None

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
                             scopes varchar,
                             expires timestamp,
                             refresh_token varchar,
                             state varchar,
                             redirect_uri varchar,
                             type varchar,
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
        c.scopes = r['scopes'].split()
        c.expires = r['expires']
        c.refreshToken = r['refresh_token']
        c.state = r['state']
        c.redirectUri = r['redirect_uri']
        c.tye = r['type']
        return c

    @classmethod
    def persist(cls, ctx, c):
        cur = ctx.con.cursor()
        try:
            p = copy.copy(c)
            p.scopes_transformed = ' '.join(p.scopes)

            if not hasattr(c, 'id') or c.id is None:
                c.id = str(uuid.uuid4())
                p.id = c.id
                cur.execute("insert into {}{} (id, client_id, user_id, token, expires, scopes, refresh_token, redirect_uri, state, type) "
                            "values (%(id)s, %(clientId)s, %(userId)s, %(token)s, %(expires)s, %(scopes_transformed)s, %(refreshToken)s, %(redirectUri)s, %(state)s, %(type)s)"
                            .format(cls._schema, cls._table),
                            p.__dict__)
            else:
                cur.execute("update {}{} set (client_id = %(clientId)s, "
                                             "user_id = %(userId)s, "
                                             "token = %(token)s, "
                                             "expires = %(expires)s, "
                                             "scopes = %(scopes_transformed)s "
                                             "refresh_token = %(refreshToken)s "
                                             "redirect_uri = %(redirectUri)s "
                                             "state = %(state)s "
                                             "type = %(type)s"
                                             "where id = %(id)s"
                            .format(cls._schema, cls._table),
                            p.__dict__)
            return c
        finally:
            cur.close()


class AuthorizationTokenSqlDAO(BaseTokenSqlDAO):

    _entity = AuthorizationToken


class BearerTokenSqlDAO(BaseTokenSqlDAO):

    _entity = BearerToken
