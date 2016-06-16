import sys
sys.path.append('../../python')
import inject
inject.configure()
import uuid
import json
import datetime
import logging

from model.registry import Registry
from model.connection.connection import Connection

from model.assistance.justifications.status import Status
from model.assistance.justifications import *
from model.assistance.justifications.justifications import Justification

from model.assistance.assistanceDao import AssistanceDAO

from model.users.users import UserDAO

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    try:
        con = conn.get()

        AssistanceDAO._createSchema(con)
        uids = [ u for (u,v) in UserDAO.findAll(con) ]
        logging.info('Usuarios')
        logging.info(uids)
        justs = Justification.getJustifications(con, uids, datetime.datetime.now() - datetime.timedelta(hours=24*60), datetime.datetime.now())
        logging.info('Justificaciones')
        logging.info([ j.status.status for j in justs ])

        con.commit()
    finally:
        conn.put(con)
