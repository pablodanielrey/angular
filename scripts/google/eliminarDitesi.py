import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor
import sys



from gauth import GAuth

#https://www.googleapis.com/auth/admin.directory.user, https://www.googleapis.com/auth/admin.directory.user.alias, https://mail.google.com/, https://www.googleapis.com/auth/drive, https://www.googleapis.com/auth/spreadsheets


SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.user',
    'https://www.googleapis.com/auth/admin.directory.user.alias',
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
    ]

SCOPESGMAIL = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/gmail.settings.sharing'
]


if __name__ == '__main__':

    admin = GAuth.getService('admin', 'directory_v1', SCOPES, 'econo@econo.unlp.edu.ar')

    import itertools
    users = []
    req = admin.users().list(domain='econo.unlp.edu.ar', query='email=ditesi@econo.unlp.edu.ar', maxResults=500)
    r = req.execute()
    users = []
    while req and 'users' in r:
        users.extend([u for u in r['users']])
        req = admin.users().list_next(previous_request=req, previous_response=r)
        if req:
            r = req.execute()
    print('se obtuvieron {} usuarios'.format(len(users)))
    for u in users:
        add = [a['address'] for a in u['emails']]
        add.remove('ditesi@econo.unlp.edu.ar')
        #print(u['primaryEmail'])
        user = {
            'emails': None
        }
        #print(user)
        print(admin.users().update(userKey=u['primaryEmail'], body=user).execute())
        #print(admin.users().aliases().delete(userKey=u['primaryEmail'], alias='ditesi@econo.unlp.edu.ar').execute())
        print('actualizado {} {}'.format(u['primaryEmail'], user))
