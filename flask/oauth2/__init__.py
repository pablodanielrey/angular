import logging
logging.getLogger('flask_oauthlib').setLevel(logging.DEBUG)
logging.getLogger('flask_oauthlib').addHandler(logging.FileHandler('/tmp/oauth.log'))

import flask
from flask import Response
from flask_oauthlib.utils import extract_params

from model.oauth.oauth2 import AuthorizationCodeGrantValidator
from oauthlib.oauth2 import WebApplicationServer


class FlaskOAuth2:

    @classmethod
    def createSchema(cls, ctx):
        from model.oauth.oauth import OAuth2Model
        OAuth2Model.createSchema(ctx)

    @classmethod
    def configureFlask(cls, ctx, app):
        server = WebApplicationServer(AuthorizationCodeGrantValidator(ctx))

        @app.route('/oauth2/authorize', methods=['GET'])
        def pre_authorize():
            uri, http_method, body, headers = extract_params()
            scopes, credentials = server.validate_authorization_request(uri, http_method, body, headers)
            logging.getLogger('flask_oauthlib').debug(scopes)
            logging.getLogger('flask_oauthlib').debug(credentials)

            ''' aca chequearía si esta logueado y lo redirijo a una página de login, etc '''

            return flask.render_template('authorize.html', credentials=credentials)

        @app.route('/oauth2/authorize', methods=['POST'])
        def post_authorize():
            uri, http_method, body, headers = extract_params()

            scopes = ['admin.users']
            credentials = {}
            """
            credentials = {
                client_id: flask.request.values.get('client_id'),
                redirect_uri: flask.request.values.get('redirect_uri'),
                response_type: flask.request.values.get('response_type'),
                state: flask.request.values.get('state')
            }
            """
            headers, body, status = server.create_authorization_response(uri, http_method, body, headers, scopes, credentials)

            ''' codigo específico de flask -- se genera la redirección '''
            response = Response(body)
            for k, v in headers.items():
                response.headers[k] = v
            response.status_code = status
            return response


        @app.route('/oauth2/access', methods=['POST'])
        def access_token():
            uri, http_method, body, headers = extract_params()
            credentials = {}
            headers, body, status = server.create_token_response(uri, http_method, body, headers, credentials)

            ''' codigo específico de flask -- se genera la redirección '''
            response = Response(body)
            for k, v in headers.items():
                response.headers[k] = v
            response.status_code = status
            return response
