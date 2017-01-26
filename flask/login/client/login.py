
from requests_oauthlib import OAuth1Session


key = 'Zziaqq0vlmMjiKefHeHNfU3y9pBRxXAafe0i0lt4DjJ87HDjfC'
secret = 'WurSJSgvdwuMparFKzSi7KyzLkDu2rOiR4vhXX5T'

request_url = 'http://127.0.0.1:5000/oauth1/request'
authorize_url = 'http://127.0.0.1:5000/oauth1/authorize'
access_url = 'http://127.0.0.1:5000/oauth1/access'

if __name__ == '__main__':
    sess = OAuth1Session(key, client_secret=secret, callback_uri='http://127.0.0.1')
    sess.fetch_request_token(request_url)
    url = sess.authorization_url(authorize_url)
    print('autorización : {}'.format(url))

    auth_code = input('código :')
    print(sess.parse_authorization_response(auth_code))
    print(sess.fetch_access_token(access_url))

    print('autorizadoooo')
