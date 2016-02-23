# -*- coding: utf-8 -*-
'''
    Crea un usuario dentro de la base de datos.

    PYTHONPATH="../../../python/model" python3 createUser.py dni name lastname

    sin email ni nada adicional.
'''
from connection import connection
from users import users
import systems
import logging


def generatePassword(con, uid):
    ''' genera una clave para el usuario si es que no tiene '''

    passw = users.UserPasswordDAO.findByUserId(con, uid)
    if len(passw) > 0:
        #logging.debug('{},ya tiene clave,'.format(uid))
        return 0

    u = users.UserDAO.findById(con, uid)
    up = users.UserPassword()
    up.userId = uid
    up.username = u.dni
    up.password = '{}-autogenerado'.format(u.dni)
    users.UserPasswordDAO.persist(con, up)
    logging.debug('{} {} {}'.format(up.userId, up.username, up.password))
    return 1


def createUser(con, dni, name, lastname):

    u = users.UserDAO.findByDni(con, dni)
    if u is not None:
        logging.warn('Persona ya existente')
        logging.warn(u)
        return

    user = users.User()
    user.name = name
    user.lastname = lastname
    user.dni = dni
    uid = users.UserDAO.persist(con, user)

    up = users.UserPassword()
    up.userId = uid
    up.username = dni
    up.password = '{}-autogenerado'.format(dni)
    users.UserPasswordDAO.persist(con, up)


if __name__ == '__main__':

    import sys

    dni = sys.argv[1]
    name = sys.argv[2]
    lastname = sys.argv[3]

    assert dni is not None
    assert name is not None
    assert lastname is not None

    import inject
    inject.configure()

    conn = inject.instance(connection.Connection)
    con = conn.get()
    try:
        createUser(con, dni, name, lastname)
        con.commit()

    finally:
        conn.put(con)
