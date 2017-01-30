
from werkzeug.security import gen_salt

import model.oauth.oauth2
from model.oauth.oauth2.entities.oauth import Client, AuthorizationToken, BearerToken

"""
from model.oauth.oauth1.entities.oauth1 import Client

class OAuth1Model:

    @classmethod
    def createClient(cls, ctx):
        c = Client()
        c.secret = gen_salt(40)
        c.key = gen_salt(50)
        c.redirectUris = ['http://127.0.0.1']
        c.persist(ctx)
        return c
"""

class OAuth2Model:

    @classmethod
    def createSchema(cls, ctx):
        ctx.getConn()
        ctx.dao(Client)._createSchema(ctx)
        ctx.dao(AuthorizationToken)._createSchema(ctx)
        ctx.dao(BearerToken)._createSchema(ctx)
        ctx.con.commit()
        ctx.closeConn()

    @classmethod
    def createClient(cls, ctx):
        from model.oauth.oauth2.entities.oauth import GRANT_TYPES
        c = Client()
        c.clientId = gen_salt(40)
        c.redirectUri = ['http://127.0.0.1/client']
        c.scopes = []
        c.grant = GRANT_TYPES[0]  # authorization_code
        c.persist(ctx)
        return c
