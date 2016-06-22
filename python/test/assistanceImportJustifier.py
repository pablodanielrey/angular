import logging
import sys
sys.path.append('../../python')

import inject
inject.configure()

import pyoo
import datetime
from model.users.users import User
from model.assistance.assistance import AssistanceModel
from model.assistance.utils import Utils

from model.registry import Registry
from model.connection.connection import Connection
from model.assistance.justifications.status import Status
from model.assistance.justifications.medicalCertificateJustification import MedicalCertificateJustification
from model.assistance.justifications.art102Justification import Art102Justification
from model.assistance.justifications.informedAbsenceJustification import InformedAbsenceJustification
from model.assistance.justifications.compensatoryJustification import CompensatoryJustification
from model.assistance.justifications.trainingJustification import TrainingJustification
from model.assistance.justifications.authorityJustification import AuthorityJustification
from model.assistance.justifications.preExamJustification import UniversityPreExamJustification
from model.assistance.justifications.outTicketJustification import OutTicketWithReturnJustification, OutTicketWithoutReturnJustification

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


class MigrateJustification():

    @classmethod
    def isJustification(cls, just):
        for c in cls.__subclasses__():
            if c.identifier == just:
                return True
        return False

class MigrateSingleJustification(MigrateJustification):


    @classmethod
    def create(cls, con, r, userId):
        j = cls.clazz.create(con, r['date'], userId, '1')
        return j

    @classmethod
    def migrateAll(cls, con, userId, justifications):
        for c in cls.__subclasses__():
            c.migrate(con, userId, justifications)

    @classmethod
    def migrate(cls, con, userId, justifications):

        for j in justifications:
            if j['just'] != cls.identifier:
                continue

            try:
                if len(cls.clazz.findByUserId(con, [userId], j['date'], j['date'])) <= 0:
                    just = cls.create(con, j, userId)
                    logging.info('persistiendo {} {}'.format(cls.identifier, just.__dict__))
                    just.persist(con)
                    just.changeStatus(con, Status.APPROVED, userId)
            except Exception as e:
                logging.info('error:{} {} {}'.format(e, j, userId))

class MigrateArt102(MigrateSingleJustification):

    identifier = "Art 102"
    clazz = Art102Justification

class MigrateInformedAbsence(MigrateSingleJustification):

    identifier = "ausente con aviso"
    clazz = InformedAbsenceJustification

class MigrateCompensatory(MigrateSingleJustification):

    identifier = "compensatorio"
    clazz = CompensatoryJustification

class MigrateTraining(MigrateSingleJustification):

    identifier = "curso de capacitacion"
    clazz = TrainingJustification

class MigrateAuthority(MigrateSingleJustification):

    identifier = "justificado por autoridad"
    clazz = AuthorityJustification

class MigrateRangedJustification(MigrateJustification):

    @classmethod
    def create(cls, con, r, userId):
        j = cls.clazz.create(con, r['date'], r['days'], userId, '1')
        return j

    @classmethod
    def migrateAll(cls, con, userId, justifications):
        for c in cls.__subclasses__():
            c.migrate(con, userId, justifications)

    @classmethod
    def migrate(cls, con, userId, justifications):
        for j in justifications:
            if j['just'] != cls.identifier:
                continue
            try:
                end = j['date'] + datetime.timedelta(days=j['days'])
                if len(cls.clazz.findByUserId(con, [userId], j['date'], end.date())) <= 0:
                    just = cls.create(con, j, userId)
                    logging.info('persistiendo {} {}'.format(cls.identifier, just.__dict__))
                    just.persist(con)
                    just.changeStatus(con, Status.APPROVED, userId)
            except Exception as e:
                logging.info('error:{} {} {}'.format(e, j, userId))

class MigrateMedCertJustification(MigrateRangedJustification):
    identifier = "justificado por médico"
    clazz = MedicalCertificateJustification

class MigratePreExamJustification(MigrateRangedJustification):
    identifier = "Pre-examen"
    clazz = UniversityPreExamJustification


class MigrateRangedTimeJustification(MigrateJustification):

    @classmethod
    def create(cls, con , r, userId):
        j = cls.clazz.create(con, r['start'], r['end'], userId, '1')
        return j

    @classmethod
    def migrateAll(cls, con, userId, justifications):
        for c in cls.__subclasses__():
            c.migrate(con, userId, justifications)

    @classmethod
    def migrate(cls, con, userId, justifications):
        for j in justifications:
            if j['just'] != cls.identifier:
                continue

            start = None if j['start'] is None else j['start'].date()
            end = None if j['end'] is None else j['end'].date()
            try:
                if len(cls.clazz.findByUserId(con, [userId], start, start)) <= 0:
                    just = cls.create(con, j, userId)
                    logging.info('persistiendo {} {}'.format(cls.identifier, just.__dict__))
                    just.persist(con)
                    just.changeStatus(con, Status.APPROVED, userId)
            except Exception as e:
                logging.info('error:{} {} {}'.format(e, j, userId))

class MigrateOutTicket(MigrateRangedTimeJustification):

    identifier = "boleta de salida"
    clazz = OutTicketWithReturnJustification

    @classmethod
    def create(cls, con, r, userId):
        if r['end'] is None:
            end = getEndSchedule(con, userId, r['start'])

            j = OutTicketWithoutReturnJustification.create(con, r['start'], end, userId, '1')
        else:
            j = cls.clazz.create(con, r['start'], r['end'], userId, '1')
        return j


def getEndSchedule(con, userId, date):
    # obtengo el schedule correspondiente
    wps = assistance.getWorkPeriods(con, [userId], date, date)
    wpsList = wps[userId]
    schedule = wpsList[0] if len(wpsList) >= 0 else None
    return None if schedule is None else schedule.getEndDate()

def localize(date):
    return Utils._localizeLocal(date)

assistance = inject.instance(AssistanceModel)

if __name__ == '__main__':

    calc = pyoo.Desktop('localhost',2002)
    doc = calc.open_spreadsheet('/tmp/justificaciones.ods')
    '''
        ordenado por dni, fecha
        fecha | Apellido | Nombre | DNI | pedido | hora entrada | hora salida
    '''

    logging.getLogger().setLevel(logging.INFO)
    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        sheet = doc.sheets[0]
        user = None
        justifications = {}
        users = []
        i = 0
        for row in sheet:
                i = i + 1
                dni = row[3].value
                if dni is None or dni == '':
                    break

                dni = str(int(dni))
                date = row[0].date
                just = row[4].value

                users.append(dni)

                startDate = None
                endDate = None
                days = 0

                logging.info('chequeando: {} {} '.format(i, just))

                if (MigrateRangedTimeJustification.isJustification(just)):
                    startDate = None if row[5].time is None else localize(datetime.datetime.combine(date.date(), row[5].time))
                    endDate = None if row[6].time is None else localize(datetime.datetime.combine(date.date(), row[6].time))

                if (MigrateRangedJustification.isJustification(just)):
                    days = None if row[5] is None else int(row[5].value)


                if dni not in justifications:
                    justifications[dni] = []

                r = {'date': date, 'just': just, 'start': startDate, 'end': endDate, 'days': days}
                justifications[dni].append(r)

        users = set(users)
        for dni in users:
            t = User.findByDni(con, dni)
            if t is None:
                userId = None
                logging.info('el usuario {} no existe en el sistema'.format(dni))
                continue
            (userId,version) =  t
            MigrateRangedJustification.migrateAll(con, userId, justifications[dni])
            MigrateSingleJustification.migrateAll(con, userId, justifications[dni])
            MigrateRangedTimeJustification.migrateAll(con, userId, justifications[dni])
        con.commit()
    finally:
        conn.put(con)
        doc.close()
