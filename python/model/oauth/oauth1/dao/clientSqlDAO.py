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

        ru = r['redirect_uris']
        c.redirectUris = ru.split() if ru else None

        ds = r['default_scopes']
        c.defaultScopes = ds.split() if ds else []
        return c

    @classmethod
    def persist(cls, ctx, c):
        cur = ctx.con.cursor()
        try:
            p = copy.copy(c)

            if len(p.defaultScopes) > 0:
                p.default_scopes_transformed = ' '.join(p.defaultScopes)
            else:
                p.default_scopes_transformed = None

            if len(p.redirectUris) > 0:
                p.redirect_uris_transformed = ' '.join(p.redirectUris)
            else:
                p.redirect_uris_transformed = None

            if not hasattr(c, 'id') or c.id is None:
                c.id = str(uuid.uuid4())
                p.id = c.id
                cur.execute("insert into {}{} (id, key, secret, redirect_uris, default_scopes) "
                            "values (%(id)s, %(key)s, %(secret)s, %(redirect_uris_transformed)s, %(default_scopes_transformed)s)"
                            .format(cls._schema, cls._table),
                            p.__dict__)
            else:
                cur.execute("update {}{} set (key = %(key)s, "
                                             "secret = %(secret)s, "
                                             "redirect_uris = %(redirect_uris_transformed)s, "
                                             "default_scopes = %(default_scopes_transformed)s) "
                                             "where id = %(id)s"
                            .format(cls._schema, cls._table),
                            p.__dict__)

            return c
        finally:
            cur.close()
