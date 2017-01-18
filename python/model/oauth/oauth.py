
from werkzeug.security import gen_salt

from model.oauth.entities.oauth import Client

class OAuth1Model:

    @classmethod
    def createClient(cls, ctx):
        c = Client()
        c.client_secret = gen_salt(40)
        c.client_key = gen_salt(50)
        c.persist(ctx)
        return c
