
from model.entity import Entity


class Client(Entity):

    TYPES = ['public','confidential']

    def __init__(self):
        self.id = None
        self.key = None
        self.secret = None
        self.redirectUris = []
        self.defaultScopes = []

    """
        propiedades que adaptan la entidad a los requerimientos de la librería flask_oauthlib

            clientgetter
                    - client_key: A random string
                    - client_secret: A random string
                    - redirect_uris: A list of redirect uris
                    - default_realms: Default scopes of the client

                    rsa_key ?????
    """

    @property
    def client_key(self):
        return self.key

    @property
    def client_secret(self):
        return self.secret

    @property
    def redirect_uris(self):
        return self.redirectUris

    @property
    def default_realms(self):
        return self.defaultScopes


class RequestToken(Entity):
    def __init__(self):
        self.id = None
        self.clientId = None
        self.userId = None
        self.token = None
        self.secret = None
        self.scopes = []
        self.redirectUri = None
        self.verifier = None

        self.client = None
        self.user = None

    """
        propiedades que adaptan a la librería flask_oauthlib

        grantgetter
            - client: Client associated with this token
            - token: Access token
            - secret: Access token secret
            - realms: Realms with this access token
            - redirect_uri: A URI for redirecting

    """

    @property
    def client_key(self):
        return self.client.client_key

    @property
    def realms(self):
        return self.scopes

    @property
    def redirect_uri(self):
        return self.redirectUri



class AccessToken(Entity):
    def __init__(self):
        self.id = None
        self.userId = None
        self.clientId = None
        self.token = None
        self.secret = None
        self.scopes = []

        self.user = None
        self.client = None

    """
        propiedades para adaptar a flask_oauthlib

        tokengetter
                - client: Client associated with this token
                - user: User associated with this token
                - token: Access token
                - secret: Access token secret
                - realms: Realms with this access token
    """

    @property
    def realms(self):
        return self.scopes



class Nonce(Entity):
    def __init__(self):
        self.id = None
        self.clientKey = None
        self.timestamp = None
        self.nonce = None
        self.requestToken = None
        self.accessToken = None

    """
        propiedades para adaptar a flask_oauthlib

        noncegetter
            - client_key: The client/consure key
            - timestamp: The ``oauth_timestamp`` parameter
            - nonce: The ``oauth_nonce`` parameter
            - request_token: Request token string, if any
            - access_token: Access token string, if any
    """

    @property
    def client_key(self):
        return self.clientKey

    @property
    def request_token(self):
        return self.requestToken

    @property
    def access_token(self):
        return self.accessToken
