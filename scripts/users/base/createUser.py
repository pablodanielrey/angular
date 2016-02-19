# -*- coding: utf-8 -*-
'''
    Crea un usuario dentro de la base de datos.
    le setea el email que debe terminar con econo.unlp.edu.ar
    no crea clave hayq ue setearsela usando changeUserPassword.py
'''
from connection import connection
from users import users
import systems
import logging

def createUser(dni, name, lastname):

    logging.getLogger().setLevel(logging.INFO)
    con = connection.getConnection()
    try:
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

        con.commit()

    finally:
        connection.closeConnection(con)


if __name__ == '__main__':

    import sys

    dni = sys.argv[1]
    name = sys.argv[2]
    lastname = sys.argv[3]

    assert dni is not None
    assert name is not None
    assert lastname is not None

    createUser(dni, name, lastname)
