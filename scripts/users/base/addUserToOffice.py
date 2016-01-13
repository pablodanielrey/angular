# -*- coding: utf-8 -*-
import connection
import groups
import users
import logging

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    import sys
    dni = sys.argv[1]
    office = sys.argv[2]

    logging.info('agregando {} a la oficina {}'.format(dni, office))

    con = connection.getConnection()
    try:
        selectedOffice = None
        offices = groups.OfficeDAO.findAll(con)
        for oid in offices:
            off = groups.OfficeDAO.findById(con, oid)
            if off.name == office:
                selectedOffice = off
                break

        if selectedOffice is None:
            logging.info('La oficina no existe')
            sys.exit(1)

        uid = users.UserDAO.findByDni(con, dni)[0]
        if uid not in selectedOffice.users:
            selectedOffice.users.append(uid)
            groups.OfficeDAO.persist(con, selectedOffice)

        logging.info('Usuarios en la oficina : {}'.format(selectedOffice.users))

        con.commit()

    finally:
        connection.closeConnection(con)
