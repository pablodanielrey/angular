import os
os.environ['DEBUG'] = 'true'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

from requests_oauthlib import OAuth2Session

clientId = 'ELkCqzXjiNzGl5f49FUTyxPuO9kIRxtLlsPOva5p'

authorize_url = 'http://127.0.0.1:5000/oauth2/authorize'
token_url = 'http://127.0.0.1:5000/oauth2/access'

client_url = 'http://127.0.0.1/client'

if __name__ == '__main__':

    sess = OAuth2Session(client_id=clientId, scope=[], redirect_uri=client_url)
    url, state = sess.authorization_url(authorize_url)
    print('Por favor ir a {}'.format(url))

    auth_code = input('código :')
    token = sess.fetch_token(token_url, authorization_response=auth_code)
    print('token : {}'.format(token))
