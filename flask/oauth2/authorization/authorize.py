
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = True
#os.environ['OAUTHLIB_STRICT_TOKEN_TYPE'] = True

from oauthlib.oauth2 import RequestValidator

from model.oauth.entities.oauth import Client

class OAuthRequestValidator(RequestValidator):

    def __init__(self, ctx):
        self.ctx = ctx

    def validate_client_id(self, client_id, request):
        try:
            return len(Client.findByIds(self.ctx, [client_id]).values) > 0
        except Exception:
            return False
