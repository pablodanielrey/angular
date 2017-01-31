from model.entity import Entity

GRANT_TYPES = ['autorization_code', 'password', 'refresh_token']
RESPONSE_TYPES = ['code', 'token']

class Client(Entity):

    TYPES = ['public', 'confidential']
    PUBLIC = 0
    CONFIDENTIAL = 1

    def __init__(self):
        self.id = None
        self.clientId = None
        self.type = self.TYPES[self.PUBLIC]
        self.redirectUri = None
        self.scopes = []
        self.grant = GRANT_TYPES[0]
        self.responseType = RESPONSE_TYPES[0]

    @property
    def client_id(self):
        return self.clientId

    @client_id.setter
    def client_id(self, value):
        self.clientId = value


class BaseToken(Entity):

    def __init__(self):
        self.id = None
        self.clientId = None
        self.userId = None
        self.token = None
        self.scopes = []
        self.expires = None
        self.type = self.__class__.__name__


class AuthorizationToken(BaseToken):

    def __init__(self):
        super().__init__()
        self.redirectUri = None
        self.refreshToken = None
        self.state = None


class BearerToken(BaseToken):

    def __init__(self):
        super().__init__()
        self.redirectUri = None
        self.refreshToken = None
        self.state = None
