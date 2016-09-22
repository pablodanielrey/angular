# -*- coding: utf-8 -*-
'''
    Por unica vez se corre para generar la info de la tabla de dovecot
'''
import connection
import users
import groups
import systems
import logging
import datetime


if __name__ == '__main__':

    ''' ahora lo comento. lo dejo aca por referencia, pero solo se debe ejecutar 1 sola vez para generar los datos principales '''
    sys.exit(1)

    uid = 2000
    ids = []

    con = connection.getConnection()
    try:
        cur = con.cursor()
        cur2 = con.cursor()
        try:
            cur.execute('select * from profile.users pu, profile.mails pm, credentials.user_password up where pu.id = pm.user_id and pu.id = up.user_id and pm.email like %s', ('%econo.unlp.edu.ar',))
            if cur.rowcount > 0:
                for du in cur:
                    if du['password'] == '12345':
                        continue

                    if du['user_id'] in ids:
                        continue

                    ids.append(du['user_id'])
                    data = {
                        'id': du['user_id'],
                        'domain': 'econo.unlp.edu.ar',
                        'home': '/home/{}'.format(du['dni']),
                        'uid': uid,
                        'gid': uid + 1,
                        'maildir': 'maildir:/home/{}/Maildir'.format(du['dni']),
                        'active': 'Y',
                        'modified': du['updated']
                    }

                    logging.info('Creando {}'.format(data['id']))
                    cur2.execute('insert into dovecot.users (user_id, domain, home, uid, gid, maildir, active, modified) values (%(id)s, %(domain)s, %(home)s, %(uid)s, %(gid)s, %(maildir)s, %(active)s, %(modified)s)', data)

                    uid = uid + 2

            con.commit()

        finally:
            cur.close()

    finally:
        connection.closeConnection(con)
