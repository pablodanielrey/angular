import copy
import uuid

from model.dao import SqlDAO
from model.oauth.entities.oauth import Client

class ClientSqlDAO(SqlDAO):

    _schema = 'oauth.'
    _table = 'client'
    _entity = Client

    @classmethod
    def _createSchema(cls, ctx):
        cur = ctx.con.cursor()
        try:
            cur.execute("create if not exists schema oauth")
            cur.execute("""create if not exists table {}{} (
                             id varchar primary key default uuid_generate_v4(),
                             client_key varchar,
                             client_secret varchar,
                             client_type varchar,
                             redirect_uris varchar,
                             default_redirect_uri varchar,
                             default_scopes varchar,
                             default_scope varchar,
                             created timestamptz default NOW()
                            )""".format(cls._schema, cls._table))
            return c
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, c, r):
        c.client_id = r['id']
        c.client_key = r['client_key']
        c.client_secret = r['client_secret']
        c.client_type = r['client_type']
        c.redirect_uris = r['redirect_uris'].split()
        c.default_redirect_uri = r['default_redirect_uri']
        c.default_scopes = r['default_scopes'].split()
        c.default_scope = r['default_scope']
        return c

    @classmethod
    def persist(cls, ctx, c):
        cur = ctx.con.cursor()
        try:
            if not hasattr(c, 'client_id'):
                c.client_id = str(uuid.uuid4())
            elif c.client_id is None:
                c.client_id = str(uuid.uuid4())
            p = copy.copy(c)
            p.default_scopes_transformed = ' '.join(p.default_scopes)
            p.redirect_uris_transpormed = ' '.join(p.redirect_uris)
            cur.execute("insert into {}{} (id, client_key, client_secret, client_type, redirect_uris, default_redirect_uri, default_scopes, default_scope) "
                        "values (%(client_id)s, %(client_key)s, %(client_secret)s, %(client_type)s, %(redirect_uris_transpormed)s, %(default_redirect_uri)s, %(default_scopes_transformed)s, %(default_scope)s)"
                        .format(cls._schema, cls._table),
                        p.__dict__)
            return c
        finally:
            cur.close()
