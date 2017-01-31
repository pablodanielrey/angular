import copy
import uuid

from model.dao import SqlDAO
from model.oauth.oauth2.entities.oauth import Client

class ClientSqlDAO(SqlDAO):

    _schema = 'oauth2.'
    _table = 'client'
    _entity = Client

    @classmethod
    def _createSchema(cls, ctx):
        cur = ctx.con.cursor()
        try:
            cur.execute("create schema if not exists {}".format(cls._schema.replace('.','')))
            cur.execute("""create table if not exists {}{} (
                             id varchar primary key default uuid_generate_v4(),
                             client_id varchar not null,
                             type varchar not null,
                             response_type varchar,
                             redirect_uri varchar,
                             scopes varchar,
                             "grant" varchar,
                             created timestamptz default NOW()
                            )""".format(cls._schema, cls._table))
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, c, r):
        c.id = r['id']
        c.clientId = r['client_id']
        c.type = r['type']
        c.redirectUri = r['redirect_uri']
        c.scopes = r['scopes'].split()
        c.grant = r['grant']
        c.responseType = r['response_type']
        return c

    @classmethod
    def persist(cls, ctx, c):
        cur = ctx.con.cursor()
        try:
            p = copy.copy(c)

            if len(p.scopes) > 0:
                p.scopes_transformed = ' '.join(p.scopes)
            else:
                p.scopes_transformed = ''

            if not hasattr(c, 'id') or c.id is None:
                c.id = str(uuid.uuid4())
                p.id = c.id
                cur.execute("""insert into {}{} (id, client_id, type, redirect_uri, scopes, "grant", response_type) """
                            "values (%(id)s, %(clientId)s, %(type)s, %(redirectUri)s, %(scopes_transformed)s, %(grant)s, %(responseType)s)"
                            .format(cls._schema, cls._table),
                            p.__dict__)
            else:
                cur.execute("update {}{} set (client_id = %(clientId)s, "
                                             "type = %(type)s, "
                                             "redirect_uri = %(redirectUri)s, "
                                             "scopes = %(scopes_transformed)s) "
                                             "response_type = %(responseType)s "
                                             """ "grant" = %(grant)s """
                                             "where id = %(id)s"
                            .format(cls._schema, cls._table),
                            p.__dict__)

            return c
        finally:
            cur.close()
