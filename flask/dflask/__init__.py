
import flask
from flask_session import Session
from functools import wraps

def logged(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'user' not in flask.session:
            return flask.redirect('/')
        else:
            return f(*args, **kwargs)
    return decorator

def configure_session(app):
    #app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_TYPE'] = 'memcached'
    Session(app)

def is_logged():
    return 'user' in flask.session

def current_user():
    return flask.session['user']

def login(user):
    flask.session['user'] = user

def logout():
    if is_logged():
        del flask.session['user']
