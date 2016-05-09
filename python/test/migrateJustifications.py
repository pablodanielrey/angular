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
from model.assistance.justifications.holidayJustification import HolidayJustification, HolidayJustificationDAO
from model.assistance.justifications.strikeJustification import StrikeJustification, StrikeJustificationDAO
from model.assistance.justifications.birthdayJustification import BirthdayJustification, BirthdayJustificationDAO
from model.assistance.justifications.bloodDonationJustification import BloodDonationJustification, BloodDonationJustificationDAO
from model.assistance.justifications.evaluationJustification import EvaluationJustification, EvaluationJustificationDAO
from model.assistance.justifications.scheduleJustification import ScheduleJustification, ScheduleJustificationDAO
from model.assistance.justifications.weatherJustification import WeatherJustification, WeatherJustificationDAO
from model.assistance.justifications.librarianDayJustification import LibrarianDayJustification, LibrarianDayJustificationDAO
from model.assistance.justifications.trainingJustification import TrainingJustification, TrainingJustificationDAO
from model.assistance.justifications.lateArrivalJustification import LateArrivalJustification, LateArrivalJustificationDAO
from model.assistance.justifications.authorityJustification import AuthorityJustification, AuthorityJustificationDAO
from model.assistance.justifications.resolution638Justification import Resolution638Justification, Resolution638JustificationDAO
from model.assistance.justifications.shortDurationJustification import ShortDurationJustification, ShortDurationJustificationDAO
from model.assistance.justifications.longDurationJustification import LongDurationJustification, LongDurationJustificationDAO
from model.assistance.justifications.familyAttentionJustification import FamilyAttentionJustification, FamilyAttentionJustificationDAO
from model.assistance.justifications.mourningJustification import MourningFirstGradeJustification, MourningSecondGradeJustification, MourningRelativeJustification, MourningJustificationDAO
from model.assistance.justifications.artJustification import ARTJustification, ARTJustificationDAO
from model.assistance.justifications.prenatalJustification import PrenatalJustification, PrenatalJustificationDAO
from model.assistance.justifications.winterBreakJustification import WinterBreakJustification, WinterBreakJustificationDAO
from model.assistance.justifications.paternityJustification import PaternityJustification, PaternityJustificationDAO
from model.assistance.justifications.maternityJustification import MaternityJustification, MaternityJustificationDAO
from model.assistance.justifications.marriageJustification import MarriageJustification, MarriageJustificationDAO
from model.assistance.justifications.leaveWithoutSalaryJustification import LeaveWithoutSalaryJustification, LeaveWithoutSalaryJustificationDAO
from model.assistance.justifications.suspensionJustification import SuspensionJustification, SuspensionJustificationDAO
from model.assistance.justifications.travelJustification import TravelJustification, TravelJustificationDAO

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
            just = InformedAbsenceJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
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
            just = CompensatoryJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
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

            if (len(just.findById(con,[just.id])) <= 0):
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
            just = Art102Justification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
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

        if cur.rowcount <= 0:
            return

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

                if (len(just.findById(con,[just.id])) <= 0):
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
        if (len(just.findById(con,[just.id])) <= 0):
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

        if cur.rowcount <= 0:
            return

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
                if (len(just.findById(con,[just.id])) <= 0):
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
        if (len(just.findById(con,[just.id])) <= 0):
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

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)
    finally:
        cur.close()


def createHoliday(con):
    """
    migra las justificaciones Feriado
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones Feriado')
        # creo la tabla
        HolidayJustificationDAO._createSchema(con)
        # id de la justificación  Feriado
        id = "5ec903fb-ddaf-4b6c-a2e8-929c77d8256f"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = HolidayJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

    finally:
        cur.close()


def createStrike(con):
    """
    migra las justificaciones Paro
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones Paro')
        # creo la tabla
        StrikeJustificationDAO._createSchema(con)
        # id de la justificación  Paro
        id = "874099dc-42a2-4941-a2e1-17398ba046fc"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = StrikeJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

    finally:
        cur.close()


def createBirthday(con):
    """
    migra las justificaciones Cumpleaños
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones Cumpleaños')
        # creo la tabla
        BirthdayJustificationDAO._createSchema(con)
        # id de la justificación  Cumpleaños
        id = "b309ea53-217d-4d63-add5-80c47eb76820"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = BirthdayJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

    finally:
        cur.close()


def createBloodDonation(con):
    """
    migra las justificaciones Donación de Sangre
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones Donación de Sangre')
        # creo la tabla
        BloodDonationJustificationDAO._createSchema(con)
        # id de la justificación  Donación de Sangre
        id = "e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = BloodDonationJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

    finally:
        cur.close()


def createEvaluation(con):
    """
    migra las justificaciones Concurso
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones Concurso')
        # creo la tabla
        EvaluationJustificationDAO._createSchema(con)
        # id de la justificación  Concurso
        id = "5289eac5-9221-4a09-932c-9f1e3d099a47"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = EvaluationJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

    finally:
        cur.close()


def createSchedule(con):
    """
    migra las justificaciones por Horario
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones Horario')
        # creo la tabla
        ScheduleJustificationDAO._createSchema(con)
        # id de la justificación  Horario
        id = "3fb52f24-3eff-4ca2-8133-c7a3abfc7262"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = ScheduleJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

    finally:
        cur.close()


def createWeather(con):
    """
    migra las justificaciones Incumbencias Climáticas
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones Incumbencias Climáticas')
        # creo la tabla
        WeatherJustificationDAO._createSchema(con)
        # id de la justificación  Incumbencias Climáticas
        id = "3d486aa0-745a-4914-a46d-bc559853d367"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = WeatherJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

    finally:
        cur.close()


def createLibrarianDay(con):
    """
    migra las justificaciones Día del Bibliotecario
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones Día del Bibliotecario')
        # creo la tabla
        LibrarianDayJustificationDAO._createSchema(con)
        # id de la justificación  Día del Bibliotecario
        id = "5c548eab-b8fc-40be-bb85-ef53d594dca9"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = LibrarianDayJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

    finally:
        cur.close()


def createTraining(con):
    """
    migra las justificaciones Asistencia a Congresos/Capacitación
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones Asistencia a Congresos/Capacitación')
        # creo la tabla
        TrainingJustificationDAO._createSchema(con)
        # id de la justificación  Asistencia a Congresos/Capacitación
        id = "508a9b3a-e326-4b77-a103-3399cb65f82a"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = TrainingJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

    finally:
        cur.close()


def createLateArrival(con):
    """
    migra las justificaciones  Entrada Tarde Justificada
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones  Entrada Tarde Justificada')
        # creo la tabla
        LateArrivalJustificationDAO._createSchema(con)
        # id de la justificación   Entrada Tarde Justificada
        id = "7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = LateArrivalJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

    finally:
        cur.close()


def createAuthority(con):
    """
    migra las justificaciones Justificado Por Autoridad
    """
    cur = con.cursor()
    try:
        logging.info('Migrando las Justificaciones Justificado Por Autoridad')
        # creo la tabla
        AuthorityJustificationDAO._createSchema(con)
        # id de la justificación  Justificado Por Autoridad
        id = "c32eb2eb-882b-4905-8e8f-c03405cee727"
        cur.execute('select id, user_id, requestor_id, jbegin, jend from assistance.justifications_requests where justification_id = %s',(id,))
        for jr in cur:
            logging.info('obteniendo justificacion : {}:{}'.format(jr['id'], jr['requestor_id']))

            userId = jr['user_id']
            ownerId = jr['requestor_id']
            date = jr['jbegin']
            just = AuthorityJustification(date, userId, ownerId)
            just.id = jr['id']

            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

    finally:
        cur.close()

def createResol638(con):
    """
        migra las justificaciones de Resolución 638
    """
    cur = con.cursor()
    try:
        logging.info("Migrando las justificaciones de Resolución 638")
        # creo la tabla
        Resolution638JustificationDAO._createSchema(con)
        # id de la justificación Resolución 638
        id = '50998530-10dd-4d68-8b4a-a4b7a87f3972'
        cur.execute('select id, user_id, requestor_id, jbegin from assistance.justifications_requests where justification_id = %s order by user_id, jbegin asc',(id,))

        if cur.rowcount <= 0:
            return

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
                just = Resolution638Justification(userId, ownerId, start, days)
                just.id = jr["id"]
                if (len(just.findById(con,[just.id])) <= 0):
                    setStatus(con, just)

                """ inicializo los datos """
                userId = jr['user_id']
                ownerId = jr['requestor_id']
                start = jr['jbegin'].date()

            end = jr['jbegin'].date()

        """ persisto el ultimo que me quedo """
        days = (end - start).days + 1
        just = Resolution638Justification(userId, ownerId, start, days)
        just.id = jr["id"]
        if (len(just.findById(con,[just.id])) <= 0):
            setStatus(con, just)

    finally:
        cur.close()

class RangedJustificationMigrate():
    """
        atributos de clase: id, dao
    """

    @classmethod
    def migrateAll(cls, con):
        for c in cls.__subclasses__():
            c.migrate(con)

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info("Se debe definir en la subclase")
        pass

    @classmethod
    def migrate(cls, con):
        cur = con.cursor()
        try:
            # creo la tabla
            cls.dao._createSchema(con)

            cur.execute('select id, user_id, requestor_id, jbegin from assistance.justifications_requests where justification_id = %s order by user_id, jbegin asc',(cls.id,))

            if cur.rowcount <= 0:
                return

            userId = None
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
                    just = cls.createJustification(userId, ownerId, start, days)
                    just.id = jr["id"]

                    if (len(just.findById(con,[just.id])) <= 0):
                        setStatus(con, just)

                    """ inicializo los datos """
                    userId = jr['user_id']
                    ownerId = jr['requestor_id']
                    start = jr['jbegin'].date()

                end = jr['jbegin'].date()

            """ persisto el ultimo que me quedo """
            days = (end - start).days + 1
            just = cls.createJustification(userId, ownerId, start, days)
            just.id = jr["id"]
            if (len(just.findById(con,[just.id])) <= 0):
                setStatus(con, just)

        finally:
            cur.close()



class ShortDurationMigrate(RangedJustificationMigrate):

    id = 'f9baed8a-a803-4d7f-943e-35c436d5db46'
    dao = ShortDurationJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando Licencia Corta Duración')
        return ShortDurationJustification(userId, ownerId, start, days)


class LongDurationMigrate(RangedJustificationMigrate):

    id = "a93d3af3-4079-4e93-a891-91d5d3145155"
    dao = LongDurationJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando Licencia Larga Duración')
        return LongDurationJustification(userId, ownerId, start, days)


class FamilyAttentionMigrate(RangedJustificationMigrate):

    id = "b80c8c0e-5311-4ad1-94a7-8d294888d770"
    dao = FamilyAttentionJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando  Licencia Médica Atención Familiar')
        return FamilyAttentionJustification(userId, ownerId, start, days)


class MourningMigrate(RangedJustificationMigrate):

    id = "0cd276aa-6d6b-4752-abe5-9258dbfd6f09"
    dao = MourningJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando  Duelo')
        return MourningFirstGradeJustification(userId, ownerId, start, days)


class ARTMigrate(RangedJustificationMigrate):

    id = "70e0951f-d378-44fb-9c43-f402cbfc63c8"
    dao = ARTJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando  ART')
        return ARTJustification(userId, ownerId, start, days)


class PrenatalMigrate(RangedJustificationMigrate):

    id = "aa41a39e-c20e-4cc4-942c-febe95569499"
    dao = PrenatalJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando  Pre natal')
        return PrenatalJustification(userId, ownerId, start, days)


class WinterBreakMigrate(RangedJustificationMigrate):

    id = "f7464e86-8b9e-4415-b370-b44b624951ca"
    dao = WinterBreakJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando  Receso de invierno')
        return WinterBreakJustification(userId, ownerId, start, days)


class PaternityMigrate(RangedJustificationMigrate):

    id = "e249bfce-5af3-4d99-8509-9adc2330700b"
    dao = PaternityJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando  Paternidad')
        return PaternityJustification(userId, ownerId, start, days)


class MaternityMigrate(RangedJustificationMigrate):

    id = "68bf4c98-984d-4b71-98b0-4165c69d62ce"
    dao = MaternityJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando  Maternidad')
        return MaternityJustification(userId, ownerId, start, days)


class MarriageMigrate(RangedJustificationMigrate):

    id = "30a249d5-f90c-4666-aec6-34c53b62a447"
    dao = MarriageJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando  Matrimonio')
        return MarriageJustification(userId, ownerId, start, days)


class LeaveWithoutSalaryMigrate(RangedJustificationMigrate):

    id = "1c14a13c-2358-424f-89d3-d639a9404579"
    dao = LeaveWithoutSalaryJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando  Licencia sin goce de sueldo')
        return LeaveWithoutSalaryJustification(userId, ownerId, start, days)


class SuspensionMigrate(RangedJustificationMigrate):

    id = "bfaebb07-8d08-4551-b264-85eb4cab6ef1"
    dao = SuspensionJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando  Suspención')
        return SuspensionJustification(userId, ownerId, start, days)


class TravelMigrate(RangedJustificationMigrate):

    id = "7747e3ff-bbe2-4f2e-88f7-9cc624a242a9"
    dao = TravelJustificationDAO

    @classmethod
    def createJustification(cls, userId, ownerId, start, days):
        logging.info('migrando  Viaje')
        return TravelJustification(userId, ownerId, start, days)


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    try:
        con = conn.get()

        createAA(con)
        createCompensatory(con)
        createBS(con)
        createArt102(con)
        createPreExam(con)
        createLAO(con)
        createTask(con)
        createHoliday(con)
        createBirthday(con)
        createStrike(con)
        createBloodDonation(con)
        createEvaluation(con)
        createSchedule(con)
        createWeather(con)
        createLibrarianDay(con)
        createTraining(con)
        createLateArrival(con)
        createAuthority(con)
        createResol638(con)
        RangedJustificationMigrate.migrateAll(con)

        con.commit()
    finally:
        conn.put(con)