import copy
import uuid

from model.dao import SqlDAO
from model.oauth.entities.oauth1 import Nonce

class NonceSqlDAO(SqlDAO):

    _schema = 'oauth.'
    _table = 'nonce'
    _entity = Nonce

    @classmethod
    def _createSchema(cls, ctx):
        cur = ctx.con.cursor()
        try:
            cur.execute("create schema if not exists {}".format(cls._schema.replace('.','')))
            cur.execute("""create table if not exists {}{} (
                             id varchar primary key default uuid_generate_v4(),
                             client_key varchar,
                             timestamp integer,
                             nonce varchar,
                             request_token varchar,
                             access_token varchar,
                             created timestamptz default NOW()
                            )""".format(cls._schema, cls._table))
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, c, r):
        c.id = r['id']
        c.clientKey = r['client_key']
        c.timestamp = ['timestamp']
        c.nonce = r['nonce']
        c.requestToken = r['request_token']
        c.accessToken = r['access_token']
        return c

    @classmethod
    def persist(cls, ctx, c):
        cur = ctx.con.cursor()
        try:
            if not hasattr(c, 'id') or c.id is None:
                c.id = str(uuid.uuid4())
                cur.execute("insert into {}{} (id, client_key, timestamp, nonce, request_token, access_token) "
                            "values (%(id)s, %(clientKey)s, %(timestamp)s, %(nonce)s, %(requestToken)s, %(accessToken)s)"
                            .format(cls._schema, cls._table),
                            c.__dict__)
            else:
                cur.execute("update {}{} set (clientKey = %(clientKey)s, "
                                             "timestamp = %(timestamp)s, "
                                             "request_token = %(requestToken)s, "
                                             "access_token = %(accessToken)s, "
                                             "nonce = %(nonce)s "
                                             "where id = %(id)s"
                            .format(cls._schema, cls._table),
                            c.__dict__)
            return c
        finally:
            cur.close()
