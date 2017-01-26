import os
os.environ['DEBUG'] = 'true'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

#from flask_oauthlib.provider import OAuth1Provider

import sys
sys.path.append('../python')
sys.path.append('.')

import flask
import dflask
import login
import app

def createApp(ctx):
    import uuid
    from flask import Flask

    app = Flask(__name__)
    app.debug = True
    app.secret_key = str(uuid.uuid4()).replace('-','')
    dflask.configure_session(app)

    return app

def configureOauth(ctx, app):
    from oauth.oauth1 import FlaskOAuth1
    FlaskOAuth1.setFlaskVars(a)
    FlaskOAuth1.setFlaskHelperHandlers(ctx, a)

    oauth1 = FlaskOAuth1.setFlaskHandlers(ctx, a)
    FlaskOAuth1.setOauthHandlers(ctx, oauth1)

def createTestingContext(host, db, u, p):
    from model import SqlContext
    import psycopg2
    import psycopg2.pool
    from psycopg2.extras import DictCursor

    pool = psycopg2.pool.ThreadedConnectionPool(1, 1, host=host, database=db, user=u, password=p, cursor_factory=DictCursor)
    ctx = SqlContext(pool)
    return ctx


if __name__ == '__main__':

    sys.path.append('.')

    h = sys.argv[1]
    d = sys.argv[2]
    u = sys.argv[3]
    p = sys.argv[4]

    pp = 5000
    if len(sys.argv) > 5:
        pp = sys.argv[5]

    ctx = createTestingContext(h,d,u,p)
    try:
        #from oauth.oauth1 import FlaskOAuth1
        #FlaskOAuth1.createSchema(ctx)
        a = createApp(ctx)
        configureOauth(ctx, a)
        login.configureRoutes(ctx, a)
        app.configureRoutes(ctx, a)
        a.run(port=pp)

    finally:
        ctx.closeAll()
