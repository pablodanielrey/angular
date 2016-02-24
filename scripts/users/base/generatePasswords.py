# -*- coding: utf-8 -*-
'''
    Genera claves para la gente que no tiene
    forma de invocacón de ejemplo:

    PYTHONPATH="../../../python/model" python3 generatePasswords.py

'''

from users import users
import sys
import inject
import logging
from connection.connection import Connection

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    count = 0
    countg = 0

    inject.configure()
    conn = inject.instance(Connection)
    con = conn.get()
    try:
        users = users.UserDAO.findAll(con)
        import createUser
        for uid, verion in users:
            logging.debug('count : {}'.format(count))
            count = count + 1
            countg = countg + createUser.generatePassword(con, uid)

        con.commit()

    finally:
        conn.put(con)


    logging.debug('cantidad total de generados : {}'.format(countg))
