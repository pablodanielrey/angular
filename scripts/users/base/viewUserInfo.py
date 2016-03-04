# -*- coding: utf-8 -*-
'''
    muestra la info de los usuarios


    PYTHONPATH="../../../python" python3 viewUserInfo.py dni

    o

    PYTHONPATH="../../../python" python3 viewUserInfo.py uid

    o

    PYTHONPATH="../../../python" python3 viewUserInfo.py dni uid


    config necesaria para el programa:

    [DEFAULT]
    ldap_server = host
    ldap_user = user
    ldap_password = passw

    [dcsys]
    host = host
    database = db
    user = user
    password = pass

    [moodle]
    host = host
    database = db
    user = user
    password = pass

'''
import sys
import inject
import logging
from model.registry import Registry
from model.connection import connection
import createUser
import addUserMail
import migrateMoodleUser
import setSystems


def _checkInLdap(reg, dni, uid):
    logging.info('Conectandose al server ldap en {}'.format(reg.get('ldap_server')))
    from ldap3 import Server, Connection, ALL_ATTRIBUTES
    s = Server(reg.get('ldap_server'))
    conn = Connection(s, user=reg.get('ldap_user'), password=reg.get('ldap_password'))
    conn.bind()
    try:
        logging.info('buscando usuario con uid = {}'.format(uid))
        if not conn.search('ou=people,dc=econo', '(|(uid={})(uid={}))'.format(uid, dni), attributes=ALL_ATTRIBUTES):
            logging.info('No existe información de ese usuario dentro del ldap')
            return None

        for e in conn.entries:
            logging.info(e.entry_get_dn())
            logging.info(e)

    finally:
        conn.unbind()

def _checkUser(dni):
    r = inject.instance(Registry)
    d = r.getRegistry('dcsys')
    conn = connection.Connection(d)
    con = conn.get()
    try:
        createUser.showUserInfo(con, dni)

    finally:
        conn.put(con)

def _checkMoodle(dni, uid):
    r = inject.instance(Registry)
    moodleR = r.getRegistry('moodle')
    conn = connection.Connection(moodleR)
    con = conn.get()
    try:
        migrateMoodleUser.showUserInfo(con, dni, uid)

    finally:
        conn.put(con)


if __name__ == '__main__':

    dni = ''
    uid = ''
    if len(sys.argv) > 2:
        dni = sys.argv[1]
        uid = sys.argv[2]
    else:
        dni = sys.argv[1]
        assert dni is not None
        if "." in dni:
            uid = dni
            dni = ''

    logging.getLogger().setLevel(logging.INFO)

    inject.configure()
    reg = inject.instance(Registry)

    logging.info('\n\n\n----- INFORMACION DEL LDAP -------')
    _checkInLdap(reg, dni, uid)

    logging.info('\n\n------ INFORMACION DEL FCE -------')
    _checkUser(dni)

    logging.info('\n\n------- INFORMACION DEL MOODLE -----')
    _checkMoodle(dni, uid)
