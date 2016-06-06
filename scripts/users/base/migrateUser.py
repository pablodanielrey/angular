# -*- coding: utf-8 -*-
'''
    migra un usuario desde la estructura vieja a la nueva de usuarios.
    o sea del ldap, al fce.
    no migra los datos de mails, etc de los sistemas de archivos de los servidores!!.

    PYTHONPATH="../../../python" python3 migrateUser.py dni name lastname uid

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



def _checkAndRemoveInLdap(reg, uid):
    '''
        chequea si existe un usuario y lo elimina
        obtiene el password y lo retorna
    '''
    logging.info('Conectandose al server ldap en {}'.format(reg.get('ldap_server')))
    from ldap3 import Server, Connection, ALL_ATTRIBUTES
    s = Server(reg.get('ldap_server'))
    conn = Connection(s, user=reg.get('ldap_user'), password=reg.get('ldap_password'))
    conn.bind()
    try:
        logging.info('buscando usuario con uid = {}'.format(uid))
        if not conn.search('ou=people,dc=econo', '(uid={})'.format(uid, uid), attributes=ALL_ATTRIBUTES):
            return None

        userPassword = None
        for e in conn.entries:
            logging.info(e.entry_get_dn())
            if 'userPassword' in e:
                userPassword = e.userPassword

            logging.info('Elimando : {}'.format(e.entry_get_dn()))
            conn.delete(e.entry_get_dn())

        return userPassword

    finally:
        conn.unbind()

def _createUser(dni, name, lastname, uid, password):
    r = inject.instance(Registry)
    d = r.getRegistry('dcsys')
    conn = connection.Connection(d)
    con = conn.get()
    try:
        createUser.createUser(con, dni, name, lastname, password)
        addUserMail.createMail(con, dni, '{}@econo.unlp.edu.ar'.format(uid))
        setSystems.setSystems(con, dni)
        con.commit()

    finally:
        conn.put(con)

def _migrateMoodle(dni, uid):
    r = inject.instance(Registry)
    moodleR = r.getRegistry('moodle')
    conn = connection.Connection(moodleR)
    con = conn.get()
    try:
        migrateMoodleUser.migrateUser(con, dni, uid)
        con.commit()

    finally:
        conn.put(con)


if __name__ == '__main__':

    dni = sys.argv[1]
    name = sys.argv[2]
    lastname = sys.argv[3]
    uid = sys.argv[4]

    assert dni is not None
    assert name is not None
    assert lastname is not None
    assert uid is not None

    logging.getLogger().setLevel(logging.INFO)
    #inject.configure()
    reg = inject.instance(Registry)

    password = _checkAndRemoveInLdap(reg, uid)
    _createUser(dni, name, lastname, uid, password)
    _migrateMoodle(dni, uid)
