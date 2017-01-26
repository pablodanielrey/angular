import logging


import flask
from flask_oauthlib.provider import oauth1, OAuth1Provider

from model.oauth.entities.oauth1 import Client, RequestToken, AccessToken, Nonce
from model.users.entities.user import User

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
        logging.getLogger('flask_oauthlib').setLevel(logging.DEBUG)
        logging.getLogger('flask_oauthlib').addHandler(logging.FileHandler('/tmp/oauth.log'))


    @classmethod
    def setFlaskHelperHandlers(cls, ctx, app):

        @app.route('/clients', methods=['GET'])
        def clients():
            ctx.getConn()
            try:
                clients = Client.find(ctx).fetch(ctx)
                return flask.render_template('client_list.html', clients=clients)

            finally:
                ctx.closeConn()

    @classmethod
    def setFlaskHandlers(cls, ctx, app):

        from flask_oauthlib.provider import OAuth1Provider
        provider = OAuth1Provider(app)
        import dflask

        @app.route('/oauth1/request', methods=['GET','POST'])
        @provider.request_token_handler
        def request_token():
            return {}

        @app.route('/oauth1/access', methods=['GET','POST'])
        @provider.access_token_handler
        def access_token():
            return {}

        @app.route('/oauth1/authorize', methods=['GET','POST'])
        @dflask.logged
        @provider.authorize_handler
        def authorize(*args, **kwargs):
            if flask.request.method == 'GET':
                ctx.getConn()
                try:
                    token = kwargs.get('resource_owner_key')
                    tokens = RequestToken.find(ctx, token=token).fetch(ctx)
                    if len(tokens) > 0:
                        kwargs['client'] = tokens[0]
                        return flask.render_template('authorize.html', **kwargs)
                    else:
                        return False
                finally:
                    ctx.closeConn()

            confirm = flask.request.form.get('confirm', 'no')
            return confirm == 'yes'

        return provider


    @classmethod
    def setOauthHandlers(cls, ctx, provider):

        def fetchRelatedTokenInfo(ctx, tk):
            ''' obtiene las entidades relacionadas de requestToken y accessToken '''
            import logging
            if tk.clientId:
                logging.getLogger('flask_oauthlib').debug('obteniendo client : {}'.format(tk.clientId))
                tk.client = Client.find(ctx, id=tk.clientId).fetch(ctx)[0]
            if tk.userId:
                logging.getLogger('flask_oauthlib').debug('obteniendo usuario : {}'.format(tk.userId))
                tk.user = User.find(ctx, id=tk.userId).fetch(ctx)[0]


        @provider.clientgetter
        def load_client(client_key=''):
            ctx.getConn()
            try:
                return Client.find(ctx, key=client_key).fetch(ctx)[0]
            finally:
                ctx.closeConn()

        @provider.grantgetter
        def load_request_token(token):
            ctx.getConn()
            try:
                tk = RequestToken.find(ctx, token=token).fetch(ctx)[0]
                fetchRelatedTokenInfo(ctx, tk)
                return tk
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
                tk.sopes = request.realms
                tk.persist(ctx)
                ctx.con.commit()

            finally:
                ctx.closeConn()

        @provider.verifiergetter
        def load_verifier(verifier, token):
            ctx.getConn()
            try:
                tk = RequestToken.find(ctx, token=token, verifier=verifier).fetch(ctx)[0]
                fetchRelatedTokenInfo(ctx, tk)
                return tk

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
            import dflask
            ctx.getConn()
            try:
                tk = RequestToken.find(ctx, token=token).fetch(ctx)[0]
                tk.verifier = verifier['oauth_verifier']
                tk.userId = dflask.current_user().id
                tk.persist(ctx)
                ctx.con.commit()

            finally:
                ctx.closeConn()

        @provider.noncegetter
        def load_nonce(client_key, timestamp, nonce, request_token, access_token):
            ctx.getConn()
            try:
                ids = Nonce.find(ctx, clientKey=client_key, timestamp=timestamp, nonce=nonce, requestToken=request_token, accessToken=access_token).fetch(ctx)
                if len(ids) <= 0:
                    return None
                else:
                    return ids[0]
            finally:
                ctx.closeConn()

        @provider.noncesetter
        def save_nonce(client_key, timestamp, nonce, request_token, access_token):
            ctx.getConn()
            try:
                n = Nonce()
                n.clientKey=client_key
                n.timestamp=timestamp
                n.nonce=nonce
                n.requestToken=request_token
                n.accessToken=access_token
                n.persist(ctx)
                ctx.con.commit()
                return n

            finally:
                ctx.closeConn()

        @provider.tokengetter
        def load_access_token(client_key, token, *args, **kwargs):
            ctx.getConn()
            try:
                tk = AccessToken.find(ctx, clientKey=client_key, token=token).fetch(ctx)[0]
                findRelatedTokenInfo(ctx, tk)
                return tk
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
            ctx.getConn()
            try:
                tk = AccessToken()
                tk.userId = request.user.id
                tk.clientId = request.client.id
                tk.token = token['oauth_token']
                tk.secret = token['oauth_token_secret']
                tk.scopes = token['oauth_authorized_realms']
                tk.persist(ctx)
                ctx.con.commit()
                return tk
            finally:
                ctx.closeConn()
