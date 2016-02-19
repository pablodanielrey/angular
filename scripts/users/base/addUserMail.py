# -*- coding: utf-8 -*-
'''
    Agrega un email a un usuario.
    Lo agrega como CONFIRMADO!!! ojo
    Forma de invocación:

        PYTHONPATH="../../../python/model" python3 addUserMail.py dni cuenta-de-email

'''
from connection import connection
from users import users
import systems
import logging

if __name__ == '__main__':

    import sys

    dni = sys.argv[1]
    email = sys.argv[2]

    assert dni is not None
    assert email is not None

    logging.getLogger().setLevel(logging.INFO)
    con = connection.getConnection()
    try:
        u = users.UserDAO.findByDni(con, dni)
        if u is None:
            logging.warn('Persona inexistente')
            sys.exit(1)

        (uid, version) = u

        mail = users.Mail()
        mail.userId = uid
        mail.email = email
        mail.confirmed = True
        mid = users.MailDAO.persist(con, mail)

        mails = users.MailDAO.findAll(con, uid)
        for m in mails:
            logging.info('{}\n'.format(m.__dict__))

        con.commit()

    finally:
        connection.closeConnection(con)
