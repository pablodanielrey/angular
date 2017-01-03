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




if __name__ == '__main__':

    host = sys.argv[1]
    db = sys.argv[2]
    duser = sys.argv[3]
    dpass = sys.argv[4]

    service = GAuth.getService('admin', 'directory_v1', SCOPES, 'econo@econo.unlp.edu.ar')
    #results = service.users().list(domain='econo.unlp.edu.ar', query='email={}@econo.unlp.edu.ar'.format(user['dni'])).execute()
    #users = results.get('users', [])

    pool = psycopg2.pool.ThreadedConnectionPool(1, 50, host=host, database=db, user=duser, password=dpass, cursor_factory=DictCursor)
    try:
        conn = pool.getconn()
        try:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            try:
                cur.execute('select dni, name, lastname, username, password, email, google '
                            'from profile.mails m left join profile.users u on (m.user_id = u.id) left join credentials.user_password up on (up.user_id = u.id) '
                            'where m.confirmed and m.email like %s and google = false', ('%econo.unlp.edu.ar',))

                for u in cur:
                    password = 'lclcynpc'
                    if len(u['password']) >= 8:
                        password = u['password']

                    user = {
                        'primaryEmail': u['dni'] + '@econo.unlp.edu.ar',
                        'name': {
                            'givenName': u['name'],
                            'familyName': u['lastname'],
                            'fullName': u['name'] + ' ' + u['lastname']
                        },
                        'password': password
                    }

                    #service.users().insert(primaryEmail='').
                    print(user)


            finally:
                cur.close()
        finally:
            pool.putconn(conn)
    finally:
        pool.closeall()
