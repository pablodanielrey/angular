# -*- coding: utf-8 -*-
'''
    Agrega un email a un usuario.
    Lo agrega como CONFIRMADO!!! ojo
    Forma de invocación:

        PYTHONPATH="../../../python" python3 addUserMail.py dni cuenta-de-email

'''
from model.connection import connection
from model.users import users
from model.registry import Registry
import createUser
import systems
import logging

def createMail(con, dni, email):
    u = users.UserDAO.findByDni(con, dni)
    if u is None:
        logging.warn('Persona inexistente')
        return

    (uid, version) = u

    emails = users.MailDAO.findAll(con, uid)
    for e in emails:
        if e.email == email:
            logging.warn('Ya tiene el email {} configurado'.format(email))
            return

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

    r = inject.instance(Registry)
    conn = connection.Connection(r.getRegistry('dcsys'))
    con = conn.get()
    try:
        createMail(con, dni, email)
        con.commit()

    finally:
        conn.put(con)
