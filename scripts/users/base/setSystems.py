# -*- coding: utf-8 -*-
'''
    Setea los sistemas del usuario especificado mediante dni
'''
import connection
import users
import systems
import logging

if __name__ == '__main__':

    import sys

    dni = sys.argv[1]
    assert dni is not None

    logging.getLogger().setLevel(logging.INFO)
    con = connection.getConnection()
    try:
        u = users.UserDAO.findByDni(con, dni)
        if u is None:
            logging.warn('Persona inexistente')
            sys.exit(1)

        (uid, version) = u
        user = users.UserDAO.findById(con, uid)
        assert user.id is not None

        domains = systems.DomainDAO.findAll(con)
        logging.info([True for d2 in domains if d2.id == uid][0])

        d = systems.Domain()
        d.id = user.id

        ''' activo los sistemas para ese usuario '''
        systems.DomainDAO.persist(con, d)

        domains = systems.DomainDAO.findAll(con)
        logging.info([True for d2 in domains if d2.id == d.id][0])

        con.rollback()

    finally:
        connection.closeConnection(con)
