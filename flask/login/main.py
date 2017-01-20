import os
os.environ['DEBUG'] = 'true'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

#from flask_oauthlib.provider import OAuth1Provider

import sys
sys.path.append('../python')



def createApp(ctx):
    import uuid
    import flask
    from flask import Flask
    from flask_session import Session

    from model import serializer
    from model.users.entities.user import User
    from model.users.entities.userPassword import UserPassword

    app = Flask(__name__)
    app.secret_key = str(uuid.uuid4()).replace('-','')
    #app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_TYPE'] = 'memcached'
    Session(app)

    @app.route('/', methods=['GET'])
    def index():
        if 'user' in flask.session:
            user = flask.session['user']
            return flask.render_template('login.html', user='{} {}'.format(user.name, user.lastname))
        else:
            return flask.render_template('login.html')

    @app.route('/login', methods=['GET','POST'])
    def login():
        if flask.request.method == 'POST':
            u = flask.request.form.get('u')
            p = flask.request.form.get('p')
            ctx.getConn()
            try:
                users = UserPassword.find(ctx, username=[u], password=[p]).fetch(ctx)
                print(users)
                for up in users:
                    print(up.__dict__)
                    user = User.find(ctx, id=[up.userId]).fetch(ctx)[0]
                    print(user.__dict__)

                    flask.session['user'] = user
                    return index()
            finally:
                ctx.closeConn()

            return flask.render_template('login.html', error='Usuario y/o Clave inválidos')

        return index()

    @app.route('/logout', methods=['GET','POST'])
    def logout():
        if 'user' in flask.session:
            flask.session.clear()
        return flask.redirect('/')

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
        app = createApp(ctx)
        app.run(port=pp)

    finally:
        ctx.closeAll()
