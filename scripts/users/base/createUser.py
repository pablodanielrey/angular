# -*- coding: utf-8 -*-
'''
    Crea un usuario dentro de la base de datos.
    le setea el email que debe terminar con econo.unlp.edu.ar
    no crea clave hayq ue setearsela usando changeUserPassword.py
'''
import connection
import users
import systems
import logging

if __name__ == '__main__':

    import sys

    dni = sys.argv[1]
    name = sys.argv[2]
    lastname = sys.argv[3]
    email = sys.argv[4]

    assert dni is not None
    assert name is not None
    assert lastname is not None
    assert email is not None and email[-17:] == 'econo.unlp.edu.ar'

    logging.getLogger().setLevel(logging.INFO)
    con = connection.getConnection()
    try:
        u = users.UserDAO.findByDni(con, dni)
        if u is not None:
            logging.warn('Persona ya existente')
            logging.warn(u)
            sys.exit(1)

        user = users.User()
        user.name = name
        user.lastname = lastname
        user.dni = dni
        uid = users.UserDAO.persist(con, user)

        mail = users.Mail()
        mail.userId = uid
        mail.email = email
        mail.confirmed = True
        mid = users.MailDAO.persist(con, mail)

        d = systems.Domain()
        d.id = uid
        systems.DomainDAO.persist(con, d)

        domains = systems.DomainDAO.findAll(con)
        logging.info([True for d2 in domains if d2.id == d.id])

        con.commit()

    finally:
        connection.closeConnection(con)
