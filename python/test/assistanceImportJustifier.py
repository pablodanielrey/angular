import logging
import sys
sys.path.append('../../python')

import inject
inject.configure()

import pyoo
import datetime
from model.users.users import User

from model.registry import Registry
from model.connection.connection import Connection
from model.assistance.justifications.medicalCertificateJustification import MedicalCertificateJustification


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


class MigrateRangedJustification():

    @classmethod
    def migrateAll(cls, con, userId, justifications):
        for c in cls.__subclasses__():
            c.migrate(con, userId, justifications)

class MigrateMedCertJustification(MigrateRangedJustification):

    identifier = "justificado por médico"

    @classmethod
    def create(cls, con, r, userId):
        # r = {'date': date, 'just': just, 'start': startDate, 'end': endDate}
        j = MedicalCertificateJustification.create(con, r['date'], 1, userId, '1')
        return j

    @classmethod
    def migrate(cls, con, userId, justifications):
        date = None
        just = None
        # r = {'date': date, 'just': just, 'start': startDate, 'end': endDate}
        for j in justifications:

            if j['just'] != cls.identifier:
                continue

            if just is None:
                just = cls.create(con, j, userId)
                date = j['date']

            if not _isContiguos(date, j['date']):
                logging.info('persistiendo {}'.format(just.__dict__))
                just.end = date
                if len(MedicalCertificateJustification.findByUserId(con, [userId], just.start, just.end)) <= 0:
                    just.persist(con)
                just = None

            date = j['date']

        if just is not None and not _isContiguos(date, j['date']):
            just.end = date
            if len(MedicalCertificateJustification.findByUserId(con, [userId], just.start, just.end)) <= 0:
                just.persist(con)


if __name__ == '__main__':

    calc = pyoo.Desktop('localhost',2002)
    doc = calc.open_spreadsheet('justificaciones.ods')
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
        for row in sheet:
                dni = row[3].value
                if dni is None or dni == '':
                    break

                dni = str(int(dni))
                date = row[0].date
                just = row[4].value

                users.append(dni)

                startDate = None if row[5].time is None else datetime.datetime.combine(date.date(), row[5].time)
                endDate = None if row[6].time is None else datetime.datetime.combine(date.date(), row[6].time)

                if dni not in justifications:
                    justifications[dni] = []

                r = {'date': date, 'just': just, 'start': startDate, 'end': endDate}
                justifications[dni].append(r)

        users = set(users)
        for dni in users:
            t = User.findByDni(con, dni)
            if t is None:
                userId = None
                logging.info('el usuario {} no existe en el sistema'.format(dni))
                continue
            (userId,version) =  t
            logging.info('{} dni: {} just: {}'.format(userId, dni, len(justifications[dni])))
            MigrateRangedJustification.migrateAll(con, userId, justifications[dni])

        con.commit()
    finally:
        conn.put(con)
        doc.close()
