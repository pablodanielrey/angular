

GRANT_TYPES = ['autorization_code', 'password', 'refresh_token']
RESPONSE_TYPES = ['code', 'token']

class Client(Entity):

    TYPES = ['public', 'confidential']
    PUBLIC = 0
    CONFIDENTIAL = 1

    def __init__(self):
        self.id = None
        self.type = self.TYPES[self.PUBLIC]
        self.redirectUri = None
        self.scopes = []
        self.grant = GRANT_TYPES[0]
        self.responseType = RESPONSE_TYPES[0]


class BaseToken(Entity):

    def __init__(self):
        self.id = None
        self.clientId = None
        self.userId = None
        self.token = None
        self.scopes = []
        self.expires = None


class AuthorizationToken(BaseToken):

    def __init__(self):
        self.redirectUri = None


class BearerToken(Entity):

    def __init__(self):
        self.refreshToken = None
        self.state = None
