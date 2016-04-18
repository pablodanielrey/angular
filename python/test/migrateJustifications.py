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
from model.assistance.justifications.compensatoryJustification import CompensatoryJustification, CompensatoryJustificationDAO
from model.assistance.justifications.outTicketJustification import OutTicketWithoutReturnJustification, OutTicketWithReturnJustification, OutTicketJustificationDAO
from model.assistance.justifications.art102Justification import Art102Justification, Art102JustificationDAO

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
    """
        Agrega el estado de las justificaciones
    """
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
    """
        migra las justificaciones Ausente con Aviso
    """
    cur = con.cursor()
    try:
        logging.info('Migrando los ausentes con aviso')
        # creo la tabla
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



def createCompensatory(con):
    """
        migra las justificaciones Compensatorio
    """
    cur = con.cursor()
    try:
        logging.info('Migrando los Compensatorios')
        # creo la tabla
        CompensatoryJustificationDAO._createSchema(con)
        # id de la justificación Compensatorio
        id = '48773fd7-8502-4079-8ad5-963618abe725'

        cur.execute('select id, user_id, requestor_id, jbegin from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = CompensatoryJustification(userId, ownerId, date)
            just.id = jr['id']
            j = just.findById(con, [just.id])
            if (j is None or len(j) <= 0):
                setStatus(con, just)

    finally:
        cur.close()

def createBS(con):
    """
        migra las justificaciones Boleta de Salida
    """
    cur = con.cursor()
    try:
        logging.info("Migrando las Boleta de Salida")
        # creo la tabla
        OutTicketJustificationDAO._createSchema(con)
        # id de la justificación Boleta de Salida
        id = 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'

        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            end = jr['jend']

            if end is None:
                just = OutTicketWithoutReturnJustification(userId, ownerId, date)
            else:
                just = OutTicketWithReturnJustification(userId, ownerId, date, end)

            just.id = jr['id']
            j = just.findById(con, [just.id])
            if (j is None or len(j) <= 0):
                setStatus(con, just)
    finally:
        cur.close()

def createArt102(con):
    """
        migra las justificaciones Artículo 102
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones Art 102')
        # creo la tabla
        Art102JustificationDAO._createSchema(con)
        # id de la justificación  Art102
        id = "4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = Art102Justification(userId, ownerId, date)
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

        # createAA(con)
        # createCompensatory(con)
        # createBS(con)
        createArt102(con)

        con.commit()
    finally:
        conn.put(con)
