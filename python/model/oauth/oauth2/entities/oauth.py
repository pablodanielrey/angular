

GRANT_TYPES = ['autorization_code', 'password', 'refresh_token']

class Client(Entity):

    TYPES = ['public', 'confidential']
    PUBLIC = 0
    CONFIDENTIAL = 1

    def __init__(self):
        self.id = None
        self.type = self.TYPES[self.PUBLIC]
        self.redirectUri = None
        self.scopes = []
        self.grants = GRANT_TYPES
        self.responseTypes = ['code', 'token']

class AuthorizationToken(Entity):

    def __init__(self):
        self.id = None
        self.clientId = None
        self.userId = None
        self.redirectUri = None
        self.scopes = []
        self.state = None
        self.code = None


class BearerToken(Entity):

    def __init__(self):
        self.id = None
        self.accessToken = None
        self.refreshToken = None
        self.clientId = None
        self.userId = None
        self.scopes = []
        self.state = None
        self.expires = None
