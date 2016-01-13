# -*- coding: utf-8 -*-
import connection
import groups
import users
import logging

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    import sys
    name = sys.argv[1]
    usrs = sys.argv[2:]

    logging.info('creando oficina\nnombre: {}\nusuarios: {}'.format(name, users))

    con = connection.getConnection()
    try:
        o = groups.Office()
        o.name = name
        o.users = []

        for u in usrs:
            user = users.UserDAO.findByDni(con, u)
            if user is None:
                logging.warn('usuario inexistente : {}'.format(u))
                continue
            (uid, version) = user
            o.users.append(uid)

        oid = groups.OfficeDAO.persist(con, o)
        office = groups.OfficeDAO.findById(con, oid)
        logging.info(office.__dict__)

        con.commit()

    finally:
        connection.closeConnection(con)
