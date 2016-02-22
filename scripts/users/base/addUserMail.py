# -*- coding: utf-8 -*-
'''
    Agrega un email a un usuario.
    Lo agrega como CONFIRMADO!!! ojo
    Forma de invocación:

        PYTHONPATH="../../../python/model" python3 addUserMail.py dni cuenta-de-email

'''
from connection import connection
import createUser
from users import users
import systems
import logging

def createMail(con, dni, email):
    u = users.UserDAO.findByDni(con, dni)
    if u is None:
        logging.warn('Persona inexistente')
        return

    (uid, version) = u

    mail = users.Mail()
    mail.userId = uid
    mail.email = email
    mail.confirmed = True
    mid = users.MailDAO.persist(con, mail)

    mails = users.MailDAO.findAll(con, uid)
    for m in mails:
        logging.info('{}\n'.format(m.__dict__))


if __name__ == '__main__':

    import sys

    dni = sys.argv[1]
    email = sys.argv[2]

    assert dni is not None
    assert email is not None

    logging.getLogger().setLevel(logging.DEBUG)

    import inject
    inject.configure()

    conn = inject.instance(connection.Connection)
    con = conn.get()
    try:
        createMail(con, dni, email)
        con.commit()

    finally:
        conn.put(con)
