# -*- coding: utf-8 -*-
'''
    Actualiza la clave y el nombre de usuario de una persona.
    El nombre de ususario queda como el dni
    La clave queda la pasada por parámetro
    en el caso de que la pesona tenga multiples usuarios y claves actualiza solo el primero.
    en el caso de que la persona no tenga usuario ni clave le crea uno.

    Forma de llamar al script

        python3 changeUserPassword.py dni clave

'''
import connection
import users
import logging

if __name__ == '__main__':

    import sys

    dni = sys.argv[1]
    passw = sys.argv[2]

    assert dni is not None
    assert passw is not None

    logging.getLogger().setLevel(logging.INFO)
    con = connection.getConnection()
    try:
        u = users.UserDAO.findByDni(con, dni)
        if u is None:
            logging.warn('Persona inexistente')
            sys.exit(1)

        (uid, version) = u
        ups = users.UserPasswordDAO.findByUserId(con, uid)
        if len(ups) <= 0:
            up = users.UserPassword()
            up.userId = uid
            up.username = dni
            up.password = passw
            users.UserPasswordDAO.persist(con, up)

        else:
            ''' actualizo el primero '''
            up = ups[0]
            up.username = dni
            up.password = passw
            users.UserPasswordDAO.persist(con, up)

        con.commit()

    finally:
        connection.closeConnection(con)
