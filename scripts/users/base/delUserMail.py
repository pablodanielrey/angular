# -*- coding: utf-8 -*-
'''
    Elimina un email a un usuario.
    Lo agrega como CONFIRMADO!!! ojo
    Forma de invocación:

        PYTHONPATH="../../../python" python3 delUserMail.py id-del-mail

'''
from model.connection import connection
from model.users import users
from model.registry import Registry
import createUser
import systems
import logging

def delMail(con, eid):
    emails = users.Mail.findByUserId(con, uid)
    assert len(emails) == 1
    emails[0].delete(con)
    logging.info('email eliminado')

if __name__ == '__main__':

    import sys

    eid = sys.argv[1]
    assert eid is not None


    logging.getLogger().setLevel(logging.DEBUG)

    import inject
    #inject.configure()

    r = inject.instance(Registry)
    conn = connection.Connection(r.getRegistry('dcsys'))
    con = conn.get()
    try:
        delMail(con, eid)
        con.commit()

    except Exception as e:
        logging.warn('Error eliminando email')
        logging.exception(e)

    finally:
        conn.put(con)
