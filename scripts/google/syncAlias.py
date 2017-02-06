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
    adminUsers = admin.users()
    adminAlias = adminUsers.aliases()


    errorTimer = 1

    """
        obtengo los usuarios creados en google, usuarios son los que van a ser configurados.
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
                cur.execute('create schema if not exists google')
                cur.execute("create table if not exists google.alias_sync ("
                    "id varchar primary key default uuid_generate_v4(), "
                    "date timestamp default NOW(), "
                    "user_id varchar not null, "
                    "dni varchar not null, "
                    "name varchar not null, "
                    "lastname varchar not null, "
                    "alias varchar not null)"
                )

                cur.execute('select u.id, dni, name, lastname, username, password, email, google '
                            'from profile.mails m left join profile.users u on (m.user_id = u.id) left join credentials.user_password up on (up.user_id = u.id) '
                            'where m.confirmed and m.email like %s order by m.email', ('%econo.unlp.edu.ar',))

                toSyncAux = cur.fetchall()

                """
                    elimino las personas que se hayan sincronizado hace menos de determinado tiempo.
                """
                cur.execute("select user_id from google.alias_sync where date + interval '7 days' > NOW()")
                toRemove = [c['user_id'] for c in cur]
                print('sacando {} usuarios de la sincronización ya que no expiró el período'.format(len(toRemove)))
                toSync = [u for u in toSyncAux if u['id'] not in toRemove and u['dni'] + '@econo.unlp.edu.ar' in users ]

                print('despues del filtrado quedaron {} usuarios a sincronizar'.format(len(toSync)))

                """
                    convierto los alias de depeco a econo. ya que gmail agrega depeco automáticamente.
                """
                for u in toSync:
                    if 'depeco.econo.unlp.edu.ar' in u['email'].lower():
                        u['email'] = u['email'].replace('depeco.econo.unlp.edu.ar', 'econo.unlp.edu.ar')


                """
                    primero genero del lado de la administración del dominio todos los alias faltantes.
                    asi le doy a google tiempo para actualizar los servidores para cuando acceda a los alias desde el lado del usuario
                """
                dirty = False

                for u in toSync:

                    if u['dni'] == '27294557':
                        continue

                    userKeyG = u['dni'] + '@econo.unlp.edu.ar'
                    if userKeyG not in users:
                        #print('ignorando usuario no existente {}'.format(userKeyG))
                        continue

                    if u['email'] in users:
                        ''' el alias ya esta configurado '''
                        continue

                    """
                        //////////////////////////////////////////
                        Ajusto el alias del lado de la administración del dominio
                        si no existe lo creo.
                        //////////////////////////////////////////
                    """
                    r = adminAlias.list(userKey=userKeyG).execute()
                    aliases = [a['alias'] for a in r.get('aliases', [])]
                    if u['email'] not in aliases:
                        print('creando alias del lado del dominio {}'.format(u['email']))
                        alias1 = {
                            'alias': u['email']
                        }
                        try:
                            r = adminAlias.insert(userKey=userKeyG, body=alias1).execute()
                        except Exception as e:
                            print(e)
                        dirty = True



                if dirty:
                    print('esperando un tiempo para darle a gmail tiempo de sincronizar datos')
                    time.sleep(120)

                """
                    Ahora accedo delegando a cada usuario y configurando el alias como cuenta predeterminada si no existe.
                """

                for u in toSync:

                    if u['dni'] == '27294557':
                        continue

                    userKeyG = u['dni'] + '@econo.unlp.edu.ar'
                    if userKeyG not in users:
                        #print('ignorando usuario no existente {}'.format(userKeyG))
                        continue

                    """
                        ///////////////////////////////////////////
                        Ajusta las preferencias del usuario de gmail para agregar el alias como predeterminado
                        ///////////////////////////////////////////
                    """
                    alias = {
                        'displayName': u['name'] + ' ' + u['lastname'],
                        'replyToAddress': u['email'],
                        'sendAsEmail': u['email'],
                        'treatAsAlias': True,
                        'isPrimary': False,
                        'isDefault': True
                    }


                    try:
                        print('accediendo a gmail con {}'.format(userKeyG))
                        gmail = GAuth.getService('gmail', 'v1', SCOPESGMAIL, userKeyG)
                        r = gmail.users().settings().sendAs().list(userId='me').execute()
                        aliases = [ a['sendAsEmail'] for a in r['sendAs'] ]
                        print('alias encontrados : {} '.format(aliases))


                        if alias['sendAsEmail'] not in aliases:
                            print('creando alias')
                            r = gmail.users().settings().sendAs().create(userId='me', body=alias).execute()
                            print(r)

                        """
                        else:
                            print('actualizando alias')
                            r = gmail.users().settings().sendAs().update(userId='me', sendAsEmail=u['email'], body=alias).execute()
                            print(r)
                        """

                        cur.execute('select user_id from google.alias_sync where user_id = %s', (u['id'],))
                        if cur.rowcount > 0:
                            cur.execute('update google.alias_sync set date = NOW() where user_id = %s', (u['id'],))
                        else:
                            cur.execute('insert into google.alias_sync (user_id, dni, name, lastname, alias) values (%s,%s,%s,%s,%s)', (u['id'], u['dni'], u['name'], u['lastname'], u['email']))

                    except Exception as e:
                        print(e)


            finally:
                cur.close()
        finally:
            pool.putconn(conn)
    finally:
        pool.closeall()
