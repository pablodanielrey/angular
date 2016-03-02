# -*- coding: utf-8 -*-
'''
    migra un usuario dentro del moodle de uid a dni.
    en el caso de que existe un dni ya como nombre de usuario, lo renombra a dni.viejo

    invocación:
        PYTHONPATH="../../../python" python3 migrateMoodleUser.py dni uid

    debe tener un registry.cfg :

    [moodle]
    host =
    database =
    user =
    password =


'''
import logging

def migrateUser(con, dni, uid):
    cur = con.cursor()
    try:
        cur.execute('select username where username = %s', (uid,))
        if cur.rowcount <= 0:
            logging.info('No existe ese usuario {}'.format(uid))
            return

        cur.execute('update mdl_user set username = %s where username = %s', ('{}.viejo'.format(dni), dni))
        if cur.rowcount > 0:
            logging.info('{} --> {}.viejo'.format(dni, dni))

        cur.execute('update mdl_user set username = %s, auth = %s where username = %s', (dni, 'fceldap', uid))
        if cur.rowcount > 0:
            logging.info('{} --> {}'.format(uid, dni))

    finally:
        cur.close()

def showUserInfo(con, dni, uid):
    import pprint
    cur = con.cursor()
    try:
        cur.execute('select id, username, email, auth from mdl_user where username = %s', (dni,))
        for c in cur:
            logging.info(pprint.pformat(c))

        cur.execute('select id, username, email, auth from mdl_user where username = %s', ('{}.viejo'.format(dni),))
        for c in cur:
            logging.info(pprint.pformat(c))

        cur.execute('select id, username, email, auth from mdl_user where username = %s', (uid,))
        for c in cur:
            logging.info(pprint.pformat(c))

    finally:
        cur.close()


if __name__ == '__main__':

    import sys
    import inject
    from model.registry import Registry
    from model.connection import connection

    dni = sys.argv[1]
    uid = sys.argv[2]

    assert dni is not None
    assert uid is not None

    inject.configure()
    r = inject.instance(Registry)
    sr = r.getRegistry('moodle')
    conn = connection.Connection(sr)
    con = conn.get()
    try:
        migrateUser(con, dni, uid)
        con.commit()

    finally:
        conn.put(con)
