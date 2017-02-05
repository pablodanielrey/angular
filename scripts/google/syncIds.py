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

    host = sys.argv[1]
    db = sys.argv[2]
    duser = sys.argv[3]
    dpass = sys.argv[4]

    admin = GAuth.getService('admin', 'directory_v1', SCOPES, 'econo@econo.unlp.edu.ar')
    #results = service.users().list(domain='econo.unlp.edu.ar', query='email={}@econo.unlp.edu.ar'.format(user['dni'])).execute()
    #users = results.get('users', [])
    adminUsers = admin.users()
    adminAlias = adminUsers.aliases()


    """
        obtengo los usuarios creados en google.
        estos usuarios son los que van a ser actualizados con los ids de los usuarios de econo.
    """
    import itertools
    users = []
    req = adminUsers.list(customer='my_customer', projection='basic', maxResults=500)
    r = req.execute()
    while req and 'users' in r:
        pusers = list(itertools.chain.from_iterable([u['emails'] for u in r['users']]))
        for u in pusers:
            if u['address'] not in users:
                users.append(u['address'])
        req = adminUsers.list_next(previous_request=req, previous_response=r)
        if req:
            r = req.execute()
    print('se obtuvieron {} usuarios'.format(len(users)))



    pool = psycopg2.pool.ThreadedConnectionPool(1, 50, host=host, database=db, user=duser, password=dpass, cursor_factory=DictCursor)
    try:
        conn = pool.getconn()
        try:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            try:
                cur.execute('select u.id, dni, name, lastname, username, password, email, google '
                            'from profile.mails m left join profile.users u on (m.user_id = u.id) left join credentials.user_password up on (up.user_id = u.id) '
                            'where m.confirmed and m.email like %s and google = false', ('%econo.unlp.edu.ar',))

                for u in cur:
                    userKeyG = u['dni'] + '@econo.unlp.edu.ar'
                    if userKeyG not in users:
                        continue

                    user = {
                        'externalIds': [
                            {
                                'type': 'custom',
                                'value': u['id']
                            }
                        ]
                    }

                    r = adminUsers.update(userKey=userKeyG, body=user).execute()
                    print(r)

            finally:
                cur.close()
        finally:
            pool.putconn(conn)
    finally:
        pool.closeall()
