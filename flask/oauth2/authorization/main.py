import os
os.environ['DEBUG'] = 'true'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

import flask
from flask import Flask
from flask_oauthlib.provider import OAuth2Provider

import sys
sys.path.append('../python')

from model.oauth.entities.oauth import Client, Grant, BearerToken


def createOauth(ctx):
    oauth = OAuth2Provider()

    @oauth.clientgetter
    def load_client(client_id):
        return Client.findByIds(ctx, [client_id])[0]

    @oauth.grantgetter
    def load_grant(client_id, code):
        return Grant.findByClientAndCode(ctx, client_id, code).fetch(ctx)[0]

    @oauth.grantsetter
    def save_grant(client_id, code, request, *args, **kwargs):
        grant = Grant()
        grant.client_id = client_id
        grant.code = code
        grant.redirect_uri = request.redirect_uri
        grant.scopes = request.scopes
        grant.expires = datetime.utcnow() + timedelta(seconds=(60 * 60 * 24 * 365))
        grant.user = request.user

    @oauth.tokengetter
    def load_token(access_token=None, refresh_token=None):
        if access_token:
            return BearerToken.findByAccessToken(ctx, access_token).fetch(ctx)[0]
        elif refresh_token:
            return BearerToken.findByRefreshToken(ctx, refresh_token).fetch(ctx)[0]

    @oauth.tokensetter
    def save_token(token, request, *args, **kwargs):
        if token['token_type'] != 'Bearer':
            raise NotImplementedError()

        for tk in BearerToken.findByUserAndClient(ctx, request.user.id, request.client_id).fetch(ctx):
            tk.delete(ctx)

        tk = BearerToken()
        tk.access_token = token['access_token']
        tk.refresh_token = token['refresh_token']
        #tk.token_type = token['token_type']
        tk.client_id = request.client.client_id
        tk.user_id = request.user.id
        tk.expires = datetime.utcnow() + timedelta(seconds=token.get('expires_in'))
        tk.scopes = token['scope'].split()

        tk.persist(ctx)

    @oauth.usergetter
    def get_user(username, password, *args, **kwargs):
        users = UserPassword.findByUsernameAndPassword(ctx, username, password).fetch(ctx)
        if len(users) <= 0:
            return None
        return users

    return oauth


def createAuthorization(app, oauth):

    @app.route('/oauth/authorize', methods=['GET','POST'])
    @oauth.authorize_handler
    def authorize_handler(*args, **kwargs):
        global logged
        if flask.request.method == 'GET':
            if logged:
                return flask.render_template('authorize.html')
            else:
                return flask.render_template('login.html')

        if flask.request.method == 'HEAD':
            response = flask.make_response('',200)
            response.headers['X-Client-ID'] = kwargs.get('client_id')
            return response

        if flask.request.method == 'POST':
            confirm = flask.request.form.get('confirm', None)
            if confirm:
                return confirm == 'yes'

            username = flask.request.form.get('username', None)
            password = flask.request.form.get('password', None)
            if username and password:
                logged = True
                return flask.render_template('authorize.html')

        raise NotImplementedError()

    @app.route('/oauth/token', methods=['POST'])
    @oauth.token_handler
    def access_token():
        return None



def createApp(oauth):
    app = Flask(__name__)
    oauth.init_app(app)

    createAuthorization(app, oauth)

    @app.route('/')
    def helloWorld():
        return "hola mundo"

    return app


if __name__ == '__main__':
    ctx = None
    oauth = createOauth(ctx)
    app = createApp(oauth)
    app.run()
