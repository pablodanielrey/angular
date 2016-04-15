
import json
import uuid
import datetime
import sys
sys.path.append('../../python')

import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection.connection import Connection
from model.assistance.assistance import AssistanceModel
from model.assistance.justifications.shortDurationJustification import ShortDurationJustification
from model.assistance.justifications.longDurationJustification import LongDurationJustification
from model.assistance.justifications.status import Status
from model.assistance.justifications.justifications import Justification

from model.serializer.utils import MySerializer, serializer_loads

from model.users.users import UserDAO


def upload(files, con):
    import pyoo
    calc = pyoo.Desktop('localhost', 2002)
    doc = calc.open_spreadsheet(files)
    try:
        sheet = doc.sheets[1]
        cur = con.cursor()
        for s in sheet:
            cuit = s[0].value
            name = s[1].value
            addr = s[2].value
            resp = s[4].value
            cont = s[5].value
            tel = s[6].value
            cms = s[7].date
            cme = s[8].date

            logging.info('cuit: {}\nnombre: {}\ndirección: {}\nresp: {}\nc start: {}\nc end:{}'.format(cuit, name, addr, resp, cms, cme))
            if cuit is None or cuit == '':
                break

            cid = str(uuid.uuid4())
            cur.execute('select id from laboral_insertion.companies where cuit = %s', (cuit,))
            if cur.rowcount <= 0:
                cur.execute('insert into laboral_insertion.companies (id, name, detail, cuit, teacher, manager, begincm, endcm)'
                            ' values (%s, %s, %s, %s, %s, %s, %s, %s)', (cid, name, '', cuit, 'Luciana Marasco', '', cms, cme))
            else:
                cid = cur.fetchone()[0]

            uid = str(uuid.uuid4())
            cur.execute('insert into laboral_insertion.contacts (id, name, email, telephone, company_id)'
                        'values (%s, %s, %s, %s, %s)', (uid, resp, cont, tel, cid))

    finally:
        doc.close()


def capitalize(con):
    cur = con.cursor()
    try:
        cur.execute('select id, name from laboral_insertion.companies')
        for c in cur.fetchall():
            cid = c['id']
            name = c['name'].title()
            cur.execute('update laboral_insertion.companies set name = %s where id = %s', (name, cid))

    finally:
        cur.close()


def _getUsers(con):
    uids = []

    uid, v = UserDAO.findByDni(con, "30001823")    # walter
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "27821597")     # maxi
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "31073351")     # ivan
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "33212183")     # santiago
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "27294557")     # pablo
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "31381082")     # ema
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "29694757")      # oporto
    uids.append(uid)

    users = UserDAO.findById(con, uids)
    return users


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        capitalize(con)
        #files = sys.argv[1]
        #logging.info('importando {}'.format(files))
        #upload(files, con)
        con.commit()

    finally:
        conn.put(con)
