
import json
import datetime
import pytz
from dateutil.tz import tzlocal
import sys
sys.path.append('../../python')

import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection.connection import Connection
from model.users.users import UserDAO

def sendMail(fn):
    from model.mail.mail import Mail
    mail = inject.instance(Mail)
    with open(fn, 'rb') as f:
        fp = mail.getFilePart('ReporteTutorias.xlsx', f.read(), content_type='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        m = mail.createMail('ditesi@econo.unlp.edu.ar', 'ditesi@econo.unlp.edu.ar', 'Reporte de Asistencia')
        m.attach(fp)
        mail._sendMail('ditesi@econo.unlp.edu.ar', ['ditesi@econo.unlp.edu.ar', 'lucas.langoni@econo.unlp.edu.ar'], m)

def toPyoo(tutorings):
    import dateutil
    import uuid
    f = str(uuid.uuid4())
    fn = '/tmp/tutorias-{}.xlsx'.format(f)

    import pyoo
    calc = pyoo.Desktop('localhost', 2002)
    doc = calc.create_spreadsheet()
    try:
        sheet = doc.sheets[0]
        i = 1

        for t in tutorings:
            for s in t.situations:
                logging.info(t.date.tzinfo)
                sheet[i,0].value = t.created.astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None) if t.created is not None else ''
                sheet[i,1].value = t.date.astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None) if t.date is not None else ''
                sheet[i,2].value = t.date.astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None) if t.date is not None else ''
                sheet[i,3].value = t.tutor.name + ' ' + t.tutor.lastname
                sheet[i,4].value = s.user['user'].name + ' ' + s.user['user'].lastname
                sheet[i,5].value = s.user['student'].studentNumber
                sheet[i,6].value = s.user['user'].dni
                sheet[i,7].value = s.situation

                i = i + 1

        doc.save(fn, pyoo.FILTER_EXCEL_2007)

    finally:
        doc.close()
    sendMail(fn)


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)

    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:

        from model.tutorias.tutorias import Tutoring
        tutorings = Tutoring.findAll(con)
        toPyoo(tutorings)

    finally:
        conn.put(con)
