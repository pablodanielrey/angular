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
    con = dovecot.getConnection()
    try:
        dcur = dcon.cursor()
        cur = con.cursor()
        try:
            dcur.execute('select modified from dovecot.users order by modified desc limit 1')

            lastSinc = None
            if dcur.rowcount <= 0:
                lastSinc = datetime.datetime.now() - datetime.timedelta(days=365)
            else:
                lastSinc = dcur['modified']
            logging.info('Fecha de la ultima actualización : {}'.format(lastSinc))

            cur.execute('select * from dovecot.users du, credentials.user_password up where du.modified > %s or up.updated > %s', (lastSinc,))
            for du in cur:
                dcur.execute('select username from dovecot.users where username = %(username)s', du)
                if dcur.rowcount <= 0:
                    logging.info('Insertando {}'.format(du['username']))
                    dcur.execute('insert into dovecot.users (username, password, domain, home, uid, gid, maildir, active, modified) values (%(username)s, %(password)s, %(domain)s, %(home)s, %(uid)s, %(gid)s, %(maildir)s, %(active)s, %(modified)s', du)
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
