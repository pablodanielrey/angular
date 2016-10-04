# -*- coding: utf-8 -*-
'''
    Elimina todos los emails que tenga registrado el usuario.

'''


def deleteAllMails(con, dni):
    u = users.UserDAO.findByDni(con, dni)
    if u is None:
        logging.warn('Persona inexistente')
        return

    (uid, version) = u
    emails = users.MailDAO.findByUserId(con, uid)
    for e in emails:
        logging.info(e.__dict__)
        users.MailDAO.delete(con, e.id)


if __name__ == '__main__':

    import sys
    import inject
    inject.configure()

    sys.path.insert(0, '../../python')

    from model.registry import Registry
    from model.connection import connection
    from model.users import users
    import logging

    dni = sys.argv[1]
    assert dni is not None

    logging.getLogger().setLevel(logging.DEBUG)


    r = inject.instance(Registry)
    conn = connection.Connection(r.getRegistry('dcsysProd'))
    con = conn.get()
    try:
        deleteAllMails(con, dni)
        con.commit()

    finally:
        conn.put(con)
