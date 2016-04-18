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
from model.assistance.justifications.informedAbsenceJustification import InformedAbsenceJustification, InformedAbsenceJustificationDAO

"""
UNDEFINED = 0
PENDING = 1
APPROVED = 2
REJECTED = 3
CANCELED = 4
"""
status = ["UNDEFINED","PENDING","APPROVED","REJECTED","CANCELED"]
def getStatus(s):
    return status.index(s)

def setStatus(con, j):
    cur = con.cursor()
    try:
        cur.execute('select * from assistance.justifications_requests_status where request_id = %s order by created asc',(j.id,))
        for s in cur:
            logging.info('obteniendo estado : {}:{}'.format(s['status'], s['request_id']))
            status = Status(s['user_id'], s['created'])
            status.status = getStatus(s['status'])
            j.setStatus(status)

            j.persist(con)
    finally:
        cur.close()

def createAA(con):
    cur = con.cursor()
    try:
        # creo el la tabla
        InformedAbsenceJustificationDAO._createSchema(con)
        # id de la justificación Ausente con Aviso
        id = 'e0dfcef6-98bb-4624-ae6c-960657a9a741'
        
        cur.execute('select id, user_id, requestor_id, jbegin from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = InformedAbsenceJustification(userId, ownerId, date)
            just.id = jr['id']
            j = just.findById(con, [just.id])
            if (j is None or len(j) <= 0):
                setStatus(con, just)

    finally:
        cur.close()

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    try:
        con = conn.get()

        createAA(con)

        con.commit()
    finally:
        conn.put(con)
