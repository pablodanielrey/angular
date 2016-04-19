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
from model.assistance.justifications.preExamJustification import UniversityPreExamJustification, SchoolPreExamJustification, PreExamJustificationDAO
from model.assistance.justifications.summerBreakJustification import SummerBreakJustification, SummerBreakJustificationDAO
from model.assistance.justifications.taskJustification import TaskWithoutReturnJustification, TaskWithReturnJustification, TaskJustificationDAO

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

def _isContiguos(date1, date2):
    """
     date.weekday() ==> 0 > Lunes, 1 > Martes, 2 > Miércoles, 3 > Jueves, 4 > Viernes, 5 > Sábado, 6 > Domingo
    """

    diff = abs((date2 - date1).days)
    if (diff <= 1):
        return True

    """ por si es fin de semana """
    if (diff <= 3 and date1.weekday() == 4):
        return True

    return False


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

            setStatus(con, just)

    finally:
        cur.close()

def createPreExam(con):
    """
        migra las justificaciones Pre-Exámen
    """
    cur = con.cursor()
    try:
        logging.info("Migrando las justificaciones de Pre-Exámen")
        # creo la tabla
        PreExamJustificationDAO._createSchema(con)
        # id de la justificación Pre Examen
        id = 'b70013e3-389a-46d4-8b98-8e4ab75335d0'
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s order by user_id, jbegin asc',(id,))

        userId = None
        ownerId = None
        start = None
        end = None
        days = 0

        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            if userId is None:
                userId = jr['user_id']
                ownerId = jr['requestor_id']
                start = jr['jbegin'].date()
                end = jr['jbegin'].date()

            """ si cambio de usuario o los dias no son contiguos persisto los datos """
            if userId != jr['user_id'] or not _isContiguos(end, jr['jbegin'].date()):
                days = (end - start).days + 1
                just = UniversityPreExamJustification(userId, ownerId, start, days)
                just.id = jr["id"]
                setStatus(con, just)

                """ inicializo los datos """
                userId = jr['user_id']
                ownerId = jr['requestor_id']
                start = jr['jbegin'].date()

            end = jr['jbegin'].date()

        """ persisto el ultimo que me quedo """
        days = (end - start).days + 1
        just = UniversityPreExamJustification(userId, ownerId, start, days)
        just.id = jr["id"]
        setStatus(con, just)

    finally:
        cur.close()


def createLAO(con):
    """
        migra las justificaciones de Licencia Anual Ordinaria
    """
    cur = con.cursor()
    try:
        logging.info("Migrando las justificaciones de LAO")
        # creo la tabla
        SummerBreakJustificationDAO._createSchema(con)
        # id de la justificación LAO
        id = '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'
        cur.execute('select id, user_id, requestor_id, jbegin from assistance.justifications_requests where justification_id = %s order by user_id, jbegin asc',(id,))

        userId = None
        ownerId = None
        start = None
        end = None
        days = 0
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            if userId is None:
                userId = jr['user_id']
                ownerId = jr['requestor_id']
                start = jr['jbegin'].date()
                end = jr['jbegin'].date()

            """ si cambio de usuario o los dias no son contiguos persisto los datos """
            if userId != jr['user_id'] or not _isContiguos(end, jr['jbegin'].date()):
                days = (end - start).days + 1
                just = SummerBreakJustification(userId, ownerId, start, days)
                just.id = jr["id"]
                setStatus(con, just)

                """ inicializo los datos """
                userId = jr['user_id']
                ownerId = jr['requestor_id']
                start = jr['jbegin'].date()

            end = jr['jbegin'].date()

        """ persisto el ultimo que me quedo """
        days = (end - start).days + 1
        just = SummerBreakJustification(userId, ownerId, start, days)
        just.id = jr["id"]
        setStatus(con, just)

    finally:
        cur.close()

def createTask(con):
    """
        migra las justificaciones Boleta en Comisión
    """
    cur = con.cursor()
    try:
        logging.info("Migrando las Boleta en Comisión")
        # creo la tabla
        TaskJustificationDAO._createSchema(con)
        # id de la justificación Boleta en Comisión
        id = 'cb2b4583-2f44-4db0-808c-4e36ee059efe'

        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            end = jr['jend']

            if end is None:
                just = TaskWithoutReturnJustification(userId, ownerId, date)
            else:
                just = TaskWithReturnJustification(userId, ownerId, date, end)

            just.id = jr['id']

            setStatus(con, just)
    finally:
        cur.close()

def createResol638(con):
    pass

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    try:
        con = conn.get()

        # createAA(con)
        # createCompensatory(con)
        # createBS(con)
        # createArt102(con)
        # createPreExam(con)
        # createLAO(con)
        createResol638(con)
        createTask(con)

        con.commit()
    finally:
        conn.put(con)
