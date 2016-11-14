import logging
import sys
sys.path.append('../../python')

import inject
inject.configure()

from model.registry import Registry
from model.connection.connection import Connection

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    ip = sys.argv[1]

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        Connection.readOnly(con)
        cur = con.cursor()
        try:
            cur.execute('select * from dhcp.vassignations where ip = %s', (ip,))
            for c in cur:
                logging.info(c)
        finally:
            cur.close()
    finally:
        conn.put(con)
