
import uuid
import json
import datetime
import sys
sys.path.append('../../python')

import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection.connection import Connection

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    connProd = Connection(reg.getRegistry('dcsysProd'))
    try:
        con = conn.get()
        conProd = connProd.get()

        cur = con.cursor()
        curProd = conProd.cursor()
        try:
            cur.execute('set timezone to %s',('UTC',))
            cur.execute('select id, user_id, justification_id, jbegin, jend, created, requestor_id from assistance.justifications_requests')
            cant = 0
            total = cur.rowcount
            for c in cur.fetchall():
                params = {
                    'id': c['id'],
                    'userId': c['user_id'],
                    'justificationId': c['justification_id'],
                    'start': c['jbegin'],
                    'end': c['jend'],
                    'created': c['created'],
                    'requestorId': c['requestor_id']
                }
                cant = cant + 1
                logging.info('insertando justification_request: {}/{}'.format(cant,total))
                curProd.execute('set timezone to %s',('UTC',))
                curProd.execute('insert into assistance.justifications_requests (id, user_id, justification_id, jbegin, jend, created, requestor_id) '
                            'values (%(id)s, %(userId)s, %(justificationId)s, %(start)s, %(end)s, %(created)s, %(requestorId)s)', params)

                cur.execute('select request_id, user_id, status, created from assistance.justifications_requests_status where request_id = %s', (c['id'],))
                for c2 in cur.fetchall():
                    params = {
                        'requestId': c2['request_id'],
                        'userId': c2['user_id'],
                        'status': c2['status'],
                        'created': c2['created']
                    }
                    curProd.execute('insert into assistance.justifications_requests_status (request_id, user_id, status, created) '
                                'values (%(requestId)s, %(userId)s, %(status)s, %(created)s)', params)

            conProd.commit()

        finally:
            cur.close()
            curProd.close()

    finally:
        conn.put(con)
        connProd.put(conProd)
