
import MySQLdb
import datetime
import sys
import logging

if __name__ == '__main__':

    host = sys.argv[1]
    user = sys.argv[2]
    passw = sys.argv[3]
    db1 = sys.argv[4]
    db2 = sys.argv[5]

    emails = set()

    logging.getLogger().setLevel(logging.DEBUG)
    logging.info('Buscando cuentas en el server origen')

    # mautic produccion
    db = MySQLdb.connect(host=host, user=user, passwd=passw, db=db1)
    try:
        cur = db.cursor()
        try:
            count = 0

            cur.execute('select email from leads where email is not null')
            for c in cur:
                emails.add(str.lower(c[0]).strip())

        finally:
            cur.close()
    finally:
        db.close()

    logging.info('Cantidad de cuentas : {}'.format(len(emails)))

    # mautic tirar
    db = MySQLdb.connect(host=host, user=user, passwd=passw, db=db2)
    try:
        cur = db.cursor()
        try:
            for email in emails:
                cur.execute('select email from leads where lower(email) = lower(%s)', (email,))
                if cur.rowcount > 0:
                    logging.info('Eliminando {}'.format(email))
                    cur.execute('delete from leads where lower(email) = lower(%s)', (email,))
                    cur.commit()

        finally:
            cur.close()
    finally:
        db.close()
