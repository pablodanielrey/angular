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
    defaultPassword = sys.argv[5]

    admin = GAuth.getService('admin', 'directory_v1', SCOPES, 'econo@econo.unlp.edu.ar')
    #results = service.users().list(domain='econo.unlp.edu.ar', query='email={}@econo.unlp.edu.ar'.format(user['dni'])).execute()
    #users = results.get('users', [])
    adminUsers = admin.users()
    adminAlias = adminUsers.aliases()



    """
        obtengo los usuarios creados en google, estos van a ser ignorados por el script.
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



    import time
    pool = psycopg2.pool.ThreadedConnectionPool(1, 50, host=host, database=db, user=duser, password=dpass, cursor_factory=DictCursor)
    try:
        conn = pool.getconn()
        try:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            try:
                cur.execute('select u.id, dni, name, lastname, username, password, email '
                            'from profile.mails m left join profile.users u on (m.user_id = u.id) left join credentials.user_password up on (up.user_id = u.id) '
                            'where m.confirmed and m.email like %s', ('%\.%econo.unlp.edu.ar',))

                uss = cur.fetchall()
                toSync = [c for c in uss if c['dni'] + '@econo.unlp.edu.ar' not in users]
                print('usuarios a sincronizar {}'.format(len(toSync)))

                for u in toSync:
                    print('analizando {}'.format(u))

                    if u['password'] is None or u['id'] is None or u['name'] is None or u['lastname'] is None or u['dni'] is None:
                        continue

                    if u['dni'] == '27294557':
                        continue

                    userKeyG = u['dni'] + '@econo.unlp.edu.ar'
                    if userKeyG in users:
                        #print('ignorando usuario existente {}'.format(userKeyG))
                        continue

                    password = defaultPassword
                    if len(u['password']) >= 8:
                        password = u['password']


                    """
                        ///////////////////////
                        agrego el usuario nuevo a google
                        ///////////////////////
                    """

                    user = {
                        'primaryEmail': userKeyG,
                        'name': {
                            'givenName': u['name'],
                            'familyName': u['lastname'],
                            'fullName': u['name'] + ' ' + u['lastname']
                        },
                        'password': password,
                        'changePasswordAtNextLogin': False,
                        'emails': [
                            {
                                'address': u['dni'] + '@econo.unlp.edu.ar',
                                'primary': True,
                                'type': 'work'
                            }
                        ],
                        'externalIds': [
                            {
                                'type': 'custom',
                                'value': u['id']
                            }
                        ]
                    }

                    print('agregando usuario {} '.format(userKeyG))
                    try:
                        r = adminUsers.insert(body=user).execute()
                        print(r)
                    except Exception as e:
                        print(e)

            finally:
                cur.close()
        finally:
            pool.putconn(conn)
    finally:
        pool.closeall()
