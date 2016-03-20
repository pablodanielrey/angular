# -*- coding: utf-8 -*-
import connection
import users
import logging

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)
    con = connection.getConnection()
    try:
        for (uid, version) in users.UserDAO.findAll(con):
            logging.info('obteniendo mails del usuario : {}'.format(uid))
            mails = users.MailDAO.findAll(con, uid)
            for m in mails:
                logging.info(m.__dict__)

    finally:
        connection.closeConnection(con)
