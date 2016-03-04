# -*- coding: utf-8 -*-
'''
    Elimina todos los emails que tenga registrado el usuario.
    Forma de invocación:

        PYTHONPATH="../../../python" python3 deleteAllMails.py dni

'''
from model.registry import Registry
from model.connection import connection
from model.users import users
import createUser
import systems
import logging


def deleteAllMails(con, dni):
    u = users.UserDAO.findByDni(con, dni)
    if u is None:
        logging.warn('Persona inexistente')
        return

    (uid, version) = u
    emails = users.MailDAO.findAll(con, uid)
    for e in emails:
        logging.info(e.__dict__)
        users.MailDAO.delete(con, e.id)


if __name__ == '__main__':

    import sys
    dni = sys.argv[1]
    assert dni is not None

    logging.getLogger().setLevel(logging.DEBUG)

    import inject
    inject.configure()

    r = inject.instance(Registry)
    conn = connection.Connection(r.getRegistry('dcsys'))
    con = conn.get()
    try:
        deleteAllMails(con, dni)
        con.commit()

    finally:
        conn.put(con)
