
from model.entity import Entity

class RequestToken(Entity):
    def __init__(self):
        self.id = None
        self.clientId = None
        self.token = None
        self.secret = None
        self.scopes = []
        self.redirect_uri = None
        self.verifier = None
        self.userId = None


class AccessToken(Entity):
    def __init__(self):
        self.id = None
        self.userId = None
        self.accessToken = None
        self.secretToken = None
        self.scopes = []


class Nonce(Entity):
    def __init__(self):
        self.id = None
        self.clientKey = None
        self.timestamp = None
        self.nonce = None
        self.requestToken = None
        self.accessToken = None
