import copy
import uuid

from model.dao import SqlDAO
from model.oauth.entities.oauth1 import Client

class ClientSqlDAO(SqlDAO):

    _schema = 'oauth.'
    _table = 'client'
    _entity = Client

    @classmethod
    def _createSchema(cls, ctx):
        cur = ctx.con.cursor()
        try:
            cur.execute("create schema if not exists {}".format(cls._schema.replace('.','')))
            cur.execute("""create table if not exists {}{} (
                             id varchar primary key default uuid_generate_v4(),
                             key varchar,
                             secret varchar,
                             redirect_uris varchar,
                             default_scopes varchar,
                             created timestamptz default NOW()
                            )""".format(cls._schema, cls._table))
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, c, r):
        c.id = r['id']
        c.key = r['key']
        c.secret = r['secret']
        c.redirectUris = r['redirect_uris'].split()
        c.defaultScopes = r['default_scopes'].split()
        return c

    @classmethod
    def persist(cls, ctx, c):
        cur = ctx.con.cursor()
        try:
            if not hasattr(c, 'id') or c.id is None:
                c.id = str(uuid.uuid4())
                p = copy.copy(c)
                p.default_scopes_transformed = ' '.join(p.defaultScopes)
                p.redirect_uris_transpormed = ' '.join(p.redirectUris)
                cur.execute("insert into {}{} (id, key, secret, redirect_uris, default_scopes) "
                            "values (%(id)s, %(key)s, %(secret)s, %(redirect_uris_transpormed)s, %(default_scopes_transformed)s)"
                            .format(cls._schema, cls._table),
                            p.__dict__)
            else:
                p = copy.copy(c)
                p.default_scopes_transformed = ' '.join(p.defaultScopes)
                p.redirect_uris_transpormed = ' '.join(p.redirectUris)
                cur.execute("update {}{} set (key = %(key)s, "
                                             "secret = %(secret)s, "
                                             "redirect_uris = %(redirect_uris_transpormed)s, "
                                             "default_scopes = %(default_scopes_transformed)s) "
                                             "where id = %(id)s"
                            .format(cls._schema, cls._table),
                            p.__dict__)

            return c
        finally:
            cur.close()
