
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


def capitalize(con):
    cur = con.cursor()
    try:
        cur.execute('select id, name, lastname from profile.users')
        for c in cur.fetchall():
            cid = c['id']
            name = c['name'].title()
            lastname = c['lastname'].title()
            cur.execute('update profile.users set name = %s, lastname = %s where id = %s', (name, lastname, cid))

    finally:
        cur.close()




if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        capitalize(con)
        con.commit()

    finally:
        conn.put(con)
