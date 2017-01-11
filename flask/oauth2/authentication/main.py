import os
os.environ['DEBUG'] = 'true'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

import flask
from flask import Flask
from flask_oauthlib.client import OAuth

import sys
sys.path.append('../python')


def createOauth(app):
    oauth = OAuth(app)




def createApp(oauth):
    app = Flask(__name__)
    #oauth.init_app(app)

    @app.route('/login', methods=['GET','POST'])
    def login():
        if flask.request.method == 'GET':
            return flask.render_template('login.html')

        if flask.request.method == 'POST':


        raise NotImplementedError()

    return app


if __name__ == '__main__':
    ctx = None
    oauth = createOauth(ctx)
    app = createApp(oauth)
    app.run()
