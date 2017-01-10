
class Grant:

    TYPES = ['authorization_code', 'password', 'client_credentials', 'refresh_token']

    def __init__(self):
        self.id = None

        self.client_id = None
        self.client = None
        self.user_id = None
        self.user = None

        self.code = None
        self.scopes = []
        self.expires = None
        self.redirect_uri = None

    def delete(self):
        return self


class Client:

    TYPES = ['public','confidential']

    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.client_type = self.TYPES[0]
        self.redirect_uris = []
        self.default_redirect_uri = None
        self.default_scopes = []
        self.default_scope = None
        self.allowed_grant_types = Grant.TYPES




class Token:

    def __init__(self):
        self.id = None
        self.clientId = None
        self.type = None
        self.accessToken = None
        self.refreshToken = None
        self.expires = None
        self.scopes = []
