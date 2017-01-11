import os
os.environ['DEBUG'] = 'true'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

import flask
from flask import Flask
from flask_oauthlib.provider import OAuth2Provider

import sys
sys.path.append('../python')

from model.users.entities.user import User
from model.users.entities.userPassword import UserPassword
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
        usersP = UserPassword.find(ctx, username=[username], password=[password]).fetch(ctx)
        if len(usersP) <= 0:
            return None
        users = User.findByIds(ctx, [usersP.values[0].userId])
        if len(users) <= 0:
            return None
        return users[0]

    return oauth


def createLogin(app, ctx):

    @app.route('/login', methods=['GET','POST'])
    def login_handler(*args, **kwargs):
        if 'user' in flask.session:
            return flask.redirect('/oauth/authorize')

        if flask.request.method == 'GET':
            return flask.render_template('login.html')

        if flask.request.method == 'POST':
            u = flask.request.form.get('username')
            p = flask.request.form.get('password')
            users = UserPassword.find(ctx, username=[u], password=[p])
            if len(users.values) <= 0:
                return flask.render_template('login.html', error='Usuario y/o Clave inválidos')

            user = users.fetch(ctx)[0]
            print(user)
            flask.session['user'] = user.userId
            flask.session.modified = True
            return flask.redirect('/oauth/authorize')

        raise NotImplementedError()

    @app.route('/logout', methods=['GET','POST'])
    def logout_handler(*args, **kwargs):
        if flask.session['user']:
            del flask.session['user']
            flask.session.modified = True
        return flask.redirect('/login')


def createAuthorization(app, oauth):

    @app.route('/oauth/authorize', methods=['GET','POST'])
    @oauth.authorize_handler
    def authorize_handler(*args, **kwargs):
        if flask.request.method == 'GET':
            return flask.render_template('authorize.html')

        if flask.request.method == 'HEAD':
            response = flask.make_response('',200)
            response.headers['X-Client-ID'] = kwargs.get('client_id')
            return response

        if flask.request.method == 'POST':
            confirm = flask.request.form.get('confirm', 'no')
            if confirm:
                return confirm == 'yes'

        raise NotImplementedError()

    @app.route('/oauth/token', methods=['POST'])
    @oauth.token_handler
    def access_token():
        return None


def createApp(oauth, ctx):
    import uuid
    app = Flask(__name__)
    app.secret_key = str(uuid.uuid4()).replace('-','')
    oauth.init_app(app)

    createLogin(app, ctx)
    createAuthorization(app, oauth)

    @app.route('/')
    def helloWorld():
        return "hola mundo"

    return app


def createTestingContext(host, db, u, p):
    from model import SqlContext
    import psycopg2
    import psycopg2.pool
    from psycopg2.extras import DictCursor

    pool = psycopg2.pool.ThreadedConnectionPool(1, 1, host=host, database=db, user=u, password=p, cursor_factory=DictCursor)
    ctx = SqlContext(pool)
    return ctx


if __name__ == '__main__':

    h = sys.argv[1]
    d = sys.argv[2]
    u = sys.argv[3]
    p = sys.argv[4]
    ctx = createTestingContext(h,d,u,p)
    ctx.getConn()
    oauth = createOauth(ctx)
    app = createApp(oauth, ctx)
    app.run()
    ctx.pool.closeall()
