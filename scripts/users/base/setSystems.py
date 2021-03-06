# -*- coding: utf-8 -*-
'''
    Setea los sistemas del usuario especificado mediante dni

    PYTHONPATH="../../../python" python3 setSystems.py dni

'''
from model.connection import connection
from model.users import users
from model.registry import Registry
import systems
import logging


def setSystems(con, dni):
    u = users.UserDAO.findByDni(con, dni)
    if u is None:
        logging.warn('insexistente')
        return

    (uid, version) = u
    luser = users.UserDAO.findById(con, [uid])
    assert len(luser) == 1

    user = luser[0]
    assert user.id is not None

    domains = systems.DomainDAO.findAll(con)
    logging.info([True for d2 in domains if d2.id == uid])

    d = systems.Domain()
    d.id = user.id

    ''' activo los sistemas para ese usuario '''
    systems.DomainDAO.persist(con, d)

    domains = systems.DomainDAO.findAll(con)
    logging.info([True for d2 in domains if d2.id == d.id])


if __name__ == '__main__':

    import sys

    dni = sys.argv[1]

    assert dni is not None

    import inject
    #inject.configure()

    r = inject.instance(Registry)
    conn = connection.Connection(r.getRegistry('dcsys'))
    con = conn.get()
    try:
        setSystems(con, dni)
        con.commit()

    finally:
        conn.put(con)
