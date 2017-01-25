
from werkzeug.security import gen_salt

from model.oauth.entities.oauth1 import Client

class OAuth1Model:

    @classmethod
    def createClient(cls, ctx):
        c = Client()
        c.secret = gen_salt(40)
        c.key = gen_salt(50)
        c.persist(ctx)
        return c
