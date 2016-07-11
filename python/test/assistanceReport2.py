
import json
import datetime
import pytz
from dateutil.tz import tzlocal
import dateutil
import sys
sys.path.append('../../python')

import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection.connection import Connection
from model.assistance.assistance import AssistanceModel
from model.assistance.statistics import WpStatistics
from model.assistance.justifications.shortDurationJustification import ShortDurationJustification
from model.assistance.justifications.longDurationJustification import LongDurationJustification
from model.assistance.justifications.status import Status
from model.assistance.justifications.justifications import Justification
from model.assistance.schedules import ScheduleDAO
from model.assistance.utils import Utils
from model.offices.offices import Office

from model.serializer.utils import MySerializer, serializer_loads

from model.users.users import UserDAO

def findUser(users, uid):
    for u in users:
        if uid == u.id:
            return u

def _secondsToHours(seconds):
    if seconds == 0:
        return ""
    else:
        return "{0:02d}:{1:02d}".format(int((seconds / 60) / 60), int((seconds / 60) % 60))

def sortOfficeUsers(users, stats):
    """
        ordena los usuarios de acuerdo a los cargos que tienen
        usa el segundo caracter del cargo como orden.
    """
    pos = {}
    pos['xxx'] = []
    for uid in users:
        if uid not in stats:
            continue

        if stats[uid][0].position is None:
            pos['xxx'].append(uid)
            continue

        if stats[uid][0].position not in pos:
            pos[stats[uid][0].position] = []
        pos[stats[uid][0].position].append(uid)

    ks = list(pos.keys())
    ks.sort(key=lambda x: x[1])

    r = []
    for k in ks:
        r.extend(pos[k])
    return r

def createZipFile(user, rp):
    import zipfile
    import os
    fn = '/tmp/reporte-asistencia-{}.zip'.format(user.dni)
    with zipfile.ZipFile(fn, mode='w', compression=zipfile.ZIP_BZIP2) as rpzip:
        for root, dir, files in os.walk(rp):
            for f in files:
                fm = '{}/{}'.format(root, f)
                logging.info('escribiendo : {}'.format(fm))
                rpzip.write(fm)
    logging.info('generado : {}'.format(fn))
    return fn

def sendMail(con, user, fn):
    logging.info('Buscando correos de {}'.format(user.dni))
    from model.users.users import Mail
    mails = Mail.findByUserId(con, user.id)
    emails = []
    for m in mails:
        emails.append(m.email)
    if len(emails) <= 0:
        return

    logging.info('enviando correos a {}'.format(emails))

    import smtplib
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email import encoders

    logging.info('leyendo archivo {}'.format(fn))
    with open(fn, 'rb') as fp:
        msg = MIMEBase('application','octet-stream')
        msg.set_payload(fp.read())
    encoders.encode_base64(msg)
    msg.add_header('Content-Disposition', 'attachment', filename='reporte-asistencia.zip')

    logging.info('enviando correo')
    outer = MIMEMultipart()
    outer['Subject'] = 'Reporte Asistencia'
    outer['From'] = 'ditesi@econo.unlp.edu.ar'
    outer['To'] = ' ,'.join(emails)
    outer.attach(msg)
    try:
        with smtplib.SMTP('163.10.17.115') as s:
            s.sendmail('ditesi@econo.unlp.edu.ar', ['pablo@econo.unlp.edu.ar','julio.ciappa@econo.unlp.edu.ar'], outer.as_string())
    except Exception as e:
        logging.exception(e)


def _getOffices(con):
    return Office.findById(con, Office.findAll(con))

def findUser(uid, users):
    for u in users:
        if u.id == uid:
            return u
    return None


def statsToPyooUser(rp, user, stats):
    if user.id not in stats:
        return

    stat = stats[user.id][0]
    justifications = {}

    import uuid
    import pyoo
    calc = pyoo.Desktop('localhost', 2002)
    doc = calc.open_spreadsheet('templateUserStats.ods')
    try:
        sheet = doc.sheets[0]
        sheet[0,1].value = user.dni
        sheet[1,1].value = user.name
        sheet[2,1].value = user.lastname
        sheet[3,1].value = stat.position

        i = 5
        for ds in stat.dailyStats:
            sheet[i,2].value = ds.date if ds.date is not None else ''
            sheet[i,3].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(ds.start)) if ds.start is not None else ''
            sheet[i,4].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(ds.end)) if ds.end is not None else ''
            sheet[i,5].value = datetime.timedelta(seconds=ds.periodSeconds) if ds.start is not None else ''
            sheet[i,6].value = ds.iin if ds.iin is not None else ''
            sheet[i,7].value = ds.out if ds.out is not None else ''
            sheet[i,8].value = datetime.timedelta(seconds=ds.workedSeconds) if ds.iin is not None else ''
            #sheet[i,9].value = datetime.timedelta(seconds=ds.workedSeconds - ds.periodSeconds) if ds.start is not None or ds.iin is not None else ''
            sheet[i,10].value = datetime.timedelta(seconds=ds.lateSeconds) if ds.lateSeconds > 0 else ''
            sheet[i,11].value = datetime.timedelta(seconds=ds.earlySeconds) if ds.earlySeconds > 0 else ''
            sheet[i,12].value = ds.justification.identifier if ds.justification is not None else ''
            sheet[i,13].value = Status.getIdentifier(ds.justification.status) if ds.justification is not None else ''

            if ds.justification is not None and ds.justification.status == 2:
                if ds.justification.identifier not in justifications:
                    justifications[ds.justification.identifier] = 1
                else:
                    justifications[ds.justification.identifier] = justifications[ds.justification.identifier] + 1

            i = i + 1

        i = i + 2
        for j in justifications.keys():
            sheet[i,0].value = j
            sheet[i,1].value = justifications[j]
            i = i + 1

        fn = '{}/{}-{}-{}.xlsx'.format(rp, user.lastname, user.name, user.dni)
        logging.info('salvando : {}'.format(fn))
        doc.save(fn, pyoo.FILTER_EXCEL_2007)

    finally:
        doc.close()



def statsToPyooOffice(rp, off, stats, users):
    rpp = '{}/{}'.format(rp, off.name)
    import os
    if not os.path.exists(rpp):
        os.makedirs(rpp)
    for uid in off.users:
        user = findUser(uid, users)
        if user:
            statsToPyooUser(rpp, user, stats)

def findOfficeByUser(uid, offices):
    off = []
    for o in offices:
        if uid in o.users:
            off.append(o)
    return off

def findOffice(oid, offices):
    for o in offices:
        if o.id == oid:
            return o

def createReportDir(user):
    import os
    newpath = '/tmp/reporte-asistencia/reporte-asistencia-{}-{}-{}'.format(user.dni, user.name, user.lastname)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    rstart = datetime.datetime.combine((datetime.datetime.now() - datetime.timedelta(days=120)).date(),datetime.time())
    rend = datetime.datetime.now()
    if len(sys.argv) >= 2:
        import dateutil
        rstart = dateutil.parser.parse(sys.argv[1], dayfirst=True)
        rend = dateutil.parser.parse(sys.argv[2], dayfirst=True)

    rstart = rstart.replace(tzinfo=dateutil.tz.tzlocal())
    rend = rend.replace(tzinfo=dateutil.tz.tzlocal())

    logging.info('Generando reporte de asistencia desde : {} hasta {}'.format(rstart, rend))

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:

        from model.assistance.assistanceDao import AssistanceDAO
        AssistanceDAO._createSchema(con)

        offices = _getOffices(con)
        offices.sort(key=lambda x: x.name)

        """ obtengo los usuarios de las oficinas """
        uids = []
        for office in offices:
            uids.extend([u for u in office.users if u not in uids])
        users = UserDAO.findById(con, uids)

        """ obtengo las estadisticas """
        logging.info('Calculando las estadísticas de {} usuarios'.format(len(uids)))
        a = inject.instance(AssistanceModel)
        stats = a.getStatistics(con, uids, rstart, rend)

        """ creo los reportes por usuario y se lo envio """
        for user in users:

            if user.id != '89d88b81-fbc0-48fa-badb-d32854d3d93a' and user.id != '0cd70f16-aebb-4274-bc67-a57da88ab6c7' and user.id != '4b89c515-2eba-4316-97b9-a6204d344d3a' and user.id != '35f7a8a6-d844-4d6f-b60b-aab810610809' and user.id != '205de802-2a15-4652-8fde-f23c674a1246':
                continue

            rp = createReportDir(user)
            statsToPyooUser(rp, user, stats)

            officesIds = Office.getOfficesByUserRole(con, user.id, tree=True, role='autoriza')
            ''' genero el reporte de esa oficina '''
            for officeId in officesIds:
                off = findOffice(officeId, offices)
                statsToPyooOffice(rp, off, stats, users)

            fn = createZipFile(user, rp)
            sendMail(con, user, fn)

    finally:
        conn.put(con)
