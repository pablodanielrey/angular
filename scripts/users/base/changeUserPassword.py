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
from model.registry import Registry
import model.connection.connection
import model.users.users
import logging
import inject

if __name__ == '__main__':

    import sys

    dni = sys.argv[1]
    passw = sys.argv[2]

    assert dni is not None
    assert passw is not None

    logging.getLogger().setLevel(logging.INFO)
    conn = model.connection.connection.Connection(inject.instance(Registry).getRegistry('dcsys'))
    con = conn.get()
    try:
        u = model.users.users.UserDAO.findByDni(con, dni)
        if u is None:
            logging.warn('Persona inexistente')
            sys.exit(1)

        (uid, version) = u
        ups = model.users.users.UserPasswordDAO.findByUserId(con, uid)
        if len(ups) <= 0:
            up = users.UserPassword()
            up.userId = uid
            up.username = dni
            up.password = passw
            model.users.users.UserPasswordDAO.persist(con, up)

        else:
            ''' actualizo el primero '''
            up = ups[0]
            up.username = dni
            up.password = passw
            model.users.users.UserPasswordDAO.persist(con, up)

        con.commit()

    finally:
        conn.put(con)
