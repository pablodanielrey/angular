
import json
import datetime
import sys
sys.path.append('../../python')

import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection.connection import Connection
from model.assistance.justifications.imapJustifier.imapJustifier import ImapJustifier

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)
    reg = inject.instance(Registry)

    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        ImapJustifier.loadJustifications(con)
        con.commit()

    finally:
        conn.put(con)
