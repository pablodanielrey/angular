# -*- coding: utf-8 -*-
'''
    Obtiene los usuarios de la base de datos principal y los crea dentro de la base del correo.
    Crea los usuarios si es que no existen en la base del dovecot y la base del sogo.
    Para el proceso de actualización solo chequea los usuarios con claves que hayan cambiado posteriormente a la ultima actualización.
'''
import connection
import dovecotConnection
import users
import groups
import systems
import logging
import datetime


if __name__ == '__main__':

    dcon = dovecotConnection.getConnection()
    con = connection.getConnection()
    try:
        dcur = dcon.cursor()
        cur = con.cursor()
        try:
            dcur.execute('select modified from dovecot.users order by modified desc limit 1')

            lastSinc = None
            if dcur.rowcount <= 0:
                lastSinc = datetime.datetime.now() - datetime.timedelta(days=365)
            else:
                lastSinc = dcur.fetchone()['modified']
            logging.info('Fecha de la ultima actualización : {}'.format(lastSinc))

            cur.execute('select du.user_id from dovecot.users du, credentials.user_password up where du.user_id = up.user_id and (du.modified > %s or up.updated > %s)', (lastSinc, lastSinc))
            logging.info('Registros encontrados {}'.format(cur.rowcount))

            usersToSync = cur.fetchall()

            for mu in usersToSync:
                logging.info('Sincronizando {}'.format(mu['user_id']))
                cur.execute('select * from profile.users pu, dovecot.users du, credentials.user_password up where pu.id = %(user_id)s, du.user_id = %(user_id)s and up.user_id = %(user_id)s', mu)
                du = cur.fetchone()
                dcur.execute('select username from dovecot.users where username = %(username)s', du)
                if dcur.rowcount <= 0:
                    logging.info('Insertando {}'.format(du['username']))
                    dcur.execute('insert into dovecot.users (username, password, domain, home, uid, gid, maildir, active, modified) values (%(username)s, %(password)s, %(domain)s, %(home)s, %(uid)s, %(gid)s, %(maildir)s, %(active)s, %(modified)s)', du)
                else:
                    logging.info('Actualizando {}'.format(du['username']))
                    dcur.execute('update dovecot.users set password = %(password)s, domain = %(domain)s, home = %(home)s, uid = %(uid)s, gid = %(gid)s, maildir = %(maildir)s, active = %(active)s, modified = %(modified)s where username = %(username)s', du)

            dcon.commit()

        finally:
            cur.close()
            dcur.close()

    finally:
        dovecotConnection.closeConnection(dcon)
        connection.closeConnection(con)
