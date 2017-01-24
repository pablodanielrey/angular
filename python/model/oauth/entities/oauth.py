
from model.entity import Entity


class Grant:

    TYPES = ['authorization_code', 'password', 'client_credentials', 'refresh_token']

    def __init__(self):
        self.id = None

        self.client_id = None
        #self.client = None
        self.user_id = None
        #self.user = None

        self.code = None
        self.scopes = []
        self.expires = None
        self.redirect_uri = None

    def delete(self):
        return self

    @classmethod
    def findByIds(cls, ctx, ids):
        return ctx.dao(cls).findByIds(ctx, ids)

    @classmethod
    def findByClientAndCode(cls, ctx, clientId, code):
        return Ids(cls, ctx.dao(cls).findByClientAndCode(ctx, clientId, code))


class Client(Entity):

    TYPES = ['public','confidential']

    def __init__(self):
        self.id = None
        self.key = None
        self.secret = None
        self.type = self.TYPES[0]
        self.redirect_uris = []
        self.default_redirect_uri = None
        self.default_scopes = []
        self.default_scope = None
        self.allowed_grant_types = Grant.TYPES

    """
        propiedades que adaptan la entidad a los requerimientos de la librería flask_oauthlib

            clientgetter
                    - client_key: A random string
                    - client_secret: A random string
                    - redirect_uris: A list of redirect uris
                    - default_realms: Default scopes of the client
    """

    @property
    def client_secret(self):
        return self.secret




class Token:

    def __init__(self):
        self.id = None
        self.access_token = None
        self.refresh_token = None
        self.expires = None
        self.scopes = []
        self.token_type = None

        self.client_id = None
        #self.client = None
        self.user_id = None
        #self.user = None

    def delete(self, ctx):
        return self

    @classmethod
    def findByIds(cls, ctx, ids):
        return ctx.dao(cls).findByIds(ctx, ids)

    @classmethod
    def findByUserAndClient(cls, ctx, userId, clientId):
        return Ids(cls, ctx.dao(cls).findByUserAndClient(ctx, userId, clientId))

    @classmethod
    def findByAccessToken(cls, ctx, token):
        return Ids(cls, ctx.dao(cls).findByAccessToken(ctx, token))


class BearerToken(Token):

    def __init__(self):
        super().__init__()
        self.token_type = 'Bearer'
