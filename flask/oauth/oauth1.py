
import flask
from flask_oauthlib.provider import OAuth1Provider

from model.oauth.entities.oauth1 import Client, RequestToken, AccessToken, Nonce

class FlaskOAuth1:

    @classmethod
    def createSchema(cls, ctx):
        ctx.getConn()
        ctx.dao(Client)._createSchema(ctx)
        ctx.dao(RequestToken)._createSchema(ctx)
        ctx.dao(AccessToken)._createSchema(ctx)
        ctx.dao(Nonce)._createSchema(ctx)
        ctx.con.commit()
        ctx.closeConn()

    @classmethod
    def setFlaskVars(cls, app):
        app.config.update({
            'OAUTH1_PROVIDER_ERROR_URI': '/oauth/errors',
            'OAUTH1_PROVIDER_REALMS': [],
            'OAUTH1_PROVIDER_ENFORCE_SSL': False,
            'OAUTH1_PROVIDER_KEY_LENGTH': (10, 100)
        })

    @classmethod
    def setFlaskHandlers(cls, ctx, app):

        from flask_oauthlib.provider import OAuth1Provider
        provider = OAuth1Provider(app)

        @app.route('/oauth1/request')
        @provider.request_token_handler
        def request_token():
            return {}

        @app.route('/oauth1/authorize', methods=['GET','POST'])
        @provider.authorize_handler
        def authorize(*args, **kwargs):
            if flask.request.method == 'GET':
                client_key = kwargs.get('resource_owner_key')
                client = Client.find(ctx, key=client_key).fetch(ctx)[0]
                kwargs['client'] = client
                return render_template('authorize.html', **kwargs)

            confirm = flask.request.form.get('confirm', 'no')
            return confirm == 'yes'

        return provider


    @classmethod
    def setOauthHandlers(cls, ctx, provider):

        @provider.clientgetter
        def load_client(key):
            ctx.getConn()
            try:
                return Client.find(ctx, key=key).fetch(ctx)[0]
            finally:
                ctx.closeConn()

        @provider.grantgetter
        def load_request_token(token):
            ctx.getConn()
            try:
                return RequestToken.find(ctx, token=token).fetch(ctx)[0]
            finally:
                ctx.closeConn()

        @provider.grantsetter
        def save_request_token(token, request):
            """
                Crear un token de acceso.
                Parámetros:
                    token = {
                        u'oauth_token': u'arandomstringoftoken',
                        u'oauth_token_secret': u'arandomstringofsecret',
                        u'oauth_authorized_realms': u'email address'
                    }
            """
            ctx.getConn()
            try:
                tk = RequestToken()
                tk.token = token['oauth_token']
                tk.secret = token['oauth_token_secret']
                tk.clientId = request.client.id
                tk.redirect_uri = request.redirect_uri
                tk.sopes = token['oauth_authorized_realms'].split()
                tk.persist(ctx)
                ctx.con.commit()

            finally:
                ctx.closeConn()

        @provider.verifiergetter
        def load_verifier(verifier, token):
            ctx.getConn()
            try:
                return RequestToken.find(ctx, token=token, verifier=verifier).fetch(ctx)[0]
            finally:
                ctx.closeConn()

        @provider.verifiersetter
        def save_verifier(token, verifier, *args, **kwargs):
            """
                Crea un verificador dado un grant
                Parámetros:
                    verifier = {
                        u'oauth_verifier': u'Gqm3id67MdkrASOCQIAlb3XODaPlun',
                        u'oauth_token': u'eTYP46AJbhp8u4LE5QMjXeItRGGoAI',
                        u'resource_owner_key': u'eTYP46AJbhp8u4LE5QMjXeItRGGoAI'            // esto es client_key
                    }
            """
            ctx.getConn()
            try:
                tk = RequestToken.find(ctx, token=token).fetch(ctx)[0]
                tk.verifier = verifier['oauth_verifier']
                tk.userId = dflask.current_user().id
                ctx.con.commit()

            finally:
                ctx.closeConn()

        @provider.noncegetter
        def load_nonce(clientKey, timestamp, nonce, requestToken, accessToken):
            ctx.getConn()
            try:
                return Nonce.find(ctx, clientKey=clientKey, timestamp=timestamp, nonce=nonce, requestToken=requestToken, accessToken=accessToken).fetch(ctx)[0]
            finally:
                ctx.closeConn()

        @provider.noncesetter
        def save_nonce(clientKey, timestamp, nonce, requestToken, accessToken):
            ctx.getConn()
            try:
                n = Nonce()
                n.clientKey=clientKey
                n.timestamp=timestamp
                n.nonce=nonce
                n.requestToken=requestToken
                n.accessToken=accessToken
                n.persist(ctx)
                ctx.con.commit()
                return n

            finally:
                ctx.closeConn()

        @provider.tokengetter
        def load_access_token(clientKey, token, *args, **kwargs):
            ctx.getConn()
            try:
                return AccessToken.find(ctx, clientKey=clientKey, token=token).fetch(ctx)[0]
            finally:
                ctx.closeConn()

        @provider.tokensetter
        def save_access_token(token, request):
            """
                token = {
                    u'oauth_token_secret': u'H1xGH4X1ZkRAulHHdLfdFm7NR350tr',
                    u'oauth_token': u'aXNlKcjkVImnTfTKj8CgFpc1XRZr6P',
                    u'oauth_authorized_realms': u'email'
                }
            """
            tk = AccessToken()
            tk.userId = request.user.id
            tk.clientId = request.client.id
            tk.token = token['oauth_token']
            tk.secret = token['oauth_token_secret']
            tk.scopes = token['oauth_authorized_realms']
            tk.persist(ctx)
            ctx.con.commit()
            return
