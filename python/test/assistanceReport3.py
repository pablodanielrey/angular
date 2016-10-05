
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
from model.positions.positions import Position

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

    name = user.name + ' ' + user.lastname + ' ' + user.dni
    logging.info('enviando correo')
    outer = MIMEMultipart()
    outer['Subject'] = 'Reporte Asistencia {}'.format(name)
    outer['From'] = 'ditesi@econo.unlp.edu.ar'
    outer['To'] = ' ,'.join(emails)
    outer.attach(msg)
    try:
        with smtplib.SMTP('163.10.17.115') as s:
            s.sendmail('ditesi@econo.unlp.edu.ar', ['pablo@econo.unlp.edu.ar'], outer.as_string())
    except Exception as e:
        logging.exception(e)


def _getOffices(con):
    offices = Office.findById(con, Office.findAll(con))
    return [ o for o in offices if o.assistance ]

def _getPositions(con, uids):
    positions = Position.findByUser(con, uids)
    return positions

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


def findPosition(uid, positions):
    ps = [p for p in positions if p.userId == uid]
    if len(ps) >= 1:
        return ps[0]
    else:
        return None

def clasifyPositions(users, positions):
    pos = {}
    for u in users:
        p = findPosition(u.id, positions)
        if p:
            if p.name not in pos:
                pos[p.name] = []
            pos[p.name].append(u)
    return pos

def getJustificationStatus(status):
    if status == 0:
        return "Indefinido"
    if status == 1:
        return "Pendiente"
    if status == 2:
        return "Aprobado"
    if status == 3:
        return "Rechazado"
    if status == 4:
        return "Cancelado"

def statsToPyooOffice(rp, off, childs, stats, users, positions):
    #@param rp

    #saco la dotación de recursos humanos.
    ousers = [ u for u in users if u.id in off.users ]
    for oooff in childs[off.id]:
        ousers.extend([ u for u in users if u.id in oooff.users ])

    cpos = clasifyPositions(ousers, positions)

    import uuid
    import pyoo
    calc = pyoo.Desktop('localhost', 2002)
    doc = calc.create_spreadsheet()
    try:
        sheet = doc.sheets[0]
        sheet[0,1].value = off.name
        sheet[1,1].value = "Dotación de Recursos Humanos"

        total = 0
        i = 3
        for n,p in list(enumerate(cpos)):
            sheet[i+n,0].value = p
            sheet[i+n,1].value = len(cpos[p])
            total = total + len(cpos[p])
            sheet[i+n,3].value = ', '.join([u.name + ' ' + u.lastname for u in cpos[p]])
        i = i + len(cpos.keys())

        sheet[i,0].value = "Total"
        sheet[i,1].value = total

        i = i + 2


        ###################################### JUSTIFICACIONES #####################################################
        for user in ousers:

            sheet[i, 0].value = user.name + ' ' + user.lastname
            i = i + 2

            sheet[i, 0].value = "Fecha"
            sheet[i, 1].value = "Entrada D"
            sheet[i, 2].value = "Llegada"
            sheet[i, 3].value = "Salida D"
            sheet[i, 4].value = "Salida"
            sheet[i, 5].value = "Horas Trabajadas"
            sheet[i, 6].value = "Justificación"
            sheet[i, 7].value = "Estado de Justficación"
            i = i + 1

            if user.id in stats:
                stat = stats[user.id][0]

                a = 0
                for s in stat.dailyStats:
                    if s.justification and s.justification.identifier:
                        sheet[i+a,0].value = s.date #fecha
                        sheet[i+a,0].number_format = 30

                        sheet[i+a,1].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.start)) if s.start else 'No declara' #hora declarada
                        sheet[i+a,1].number_format = 41

                        sheet[i+a,2].value = s.iin if s.iin else ''
                        if sheet[i+a,2].value != '':
                            sheet[i+a,2].number_format = 41

                        sheet[i+a,3].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.end)) if s.end else 'No declara' # hroa declarada
                        if sheet[i+a,3].value != 'No declara':
                            sheet[i+a,3].number_format = 41

                        sheet[i+a,4].value = s.out if s.out else ''
                        if sheet[i+a,4].value != '':
                            sheet[i+a,4].number_format = 41

                        sheet[i+a,5].value = (s.out - s.iin) if s.out and s.iin else '' #horas trabajadas
                        sheet[i+a,6].value = s.justification.identifier if s and s.justification else ''
                        sheet[i+a,7].value = getJustificationStatus(s.justification.status) if s and s.justification else ''
                        a = a + 1
                i = i + a + 2

            sheet[i,0].value = 'Justificación'
            sheet[i,1].value = 'Cantidad'

            i = i + 1
            if user.id in stats:
                stat = stats[user.id][0]

                justs = {}
                for s in stat.dailyStats:
                    if s.justification and s.justification.identifier:
                        if s.justification.identifier not in justs:
                            justs[s.justification.identifier] = 0
                        justs[s.justification.identifier] = justs[s.justification.identifier] + 1

                for n,j in enumerate(justs.keys()):
                    sheet[i+n,0].value = j
                    sheet[i+n,1].value = justs[j]


                i = i + len(justs.keys()) + 3

            ##############################################  INCUMPLIMIENTOS #######################################

            sheet[i+2, 0].value = "Incumplimientos"
            sheet[i+3, 0].value = "Fecha"
            sheet[i+3, 1].value = "Entrada D"
            sheet[i+3, 2].value = "Llegada"
            sheet[i+3, 3].value = "Salida D"
            sheet[i+3, 4].value = "Salida"
            sheet[i+3, 5].value = "Falta"
            sheet[i+3, 6].value = "Diferencia"
            sheet[i+3, 7].value = "Horas Trabajadas"
            sheet[i+3, 8].value = "Justificación"
            sheet[i+3, 9].value = "Estado de Justficación"

            i = i + 1

            if user.id in stats:
                stat = stats[user.id][0]

                for s in stat.dailyStats:

                    """
                            UNDEFINED = 0
                            PENDING = 1
                            APPROVED = 2
                            REJECTED = 3
                            CANCELED = 4
                    """
                    #if s.justification and s.justification.status and s.justification.status == 2:
                    #    # justificaciones aprobadas
                    #    continue
                    if s.justification and s.justification.identifier:
                        continue


                    #chequeo si tiene inclumplimento
                    if s.start and s.iin is None:

                        if s.out is None and user.id in cpos.keys() and '2' in cpos[user.id]:
                            sheet[i+3,0].value = s.date #fecha
                            sheet[i+3,0].number_format = 30

                            sheet[i+3,1].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.start)) #hora declarada
                            sheet[i+3,1].number_format = 41

                            sheet[i+3,3].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.end)) if s.end else 'No declara' # hroa declarada
                            if sheet[i+3,3].value != 'No declara':
                                sheet[i+3,3].number_format = 41

                            sheet[i+3,5].value = 'No Marcó'
                            sheet[i+3,8].value = s.justification.identifier if s and s.justification else ''
                            sheet[i+3,9].value = s.justification.status if s and s.justification else ''
                            i = i + 1
                            continue

                        else:
                            sheet[i+3,0].value = s.date #fecha
                            sheet[i+3,0].number_format = 30

                            sheet[i+3,1].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.start)) #hora declarada
                            sheet[i+3,1].number_format = 41

                            sheet[i+3,3].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.end)) if s.end else 'No declara' # hroa declarada
                            if sheet[i+3,3].value != 'No declara':
                                sheet[i+3,3].number_format = 41

                            sheet[i+3,5].value = 'Inasistencia'
                            sheet[i+3,8].value = s.justification.identifier if s and s.justification else ''
                            sheet[i+3,9].value = s.justification.status if s and s.justification else ''
                            i = i + 1
                            continue

                    if user.id in cpos.keys() and '2' in cpos[user.id]:
                        #es director. marca prescencia
                        continue

                    #chequeo si tiene inclumplimento
                    if s.end and s.out is None:
                        sheet[i+3,0].value = s.date #fecha
                        sheet[i+3,0].number_format = 30

                        sheet[i+3,1].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.start)) #hora declarada
                        sheet[i+3,1].number_format = 41

                        sheet[i+3,2].value = s.iin
                        sheet[i+3,2].number_format = 41

                        sheet[i+3,3].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.end)) if s.end else 'No declara' # hroa declarada
                        if sheet[i+3,3].value != 'No declara':
                            sheet[i+3,3].number_format = 41

                        sheet[i+3,5].value = 'No marcó salida'
                        sheet[i+3,8].value = s.justification.identifier if s and s.justification else ''
                        sheet[i+3,9].value = s.justification.status if s and s.justification else ''
                        i = i + 1
                        continue

                    if s.workedSeconds >= ((60 * 60 * 6) + (30 * 60)):
                        #cumplió las 6:30 horas
                        continue;


                    tolerancia = datetime.timedelta(seconds=(60 * 15))
                    #chequeo si tiene inclumplimento
                    if s.start and s.iin and s.iin > Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.start)) + tolerancia:
                        sheet[i+3,0].value = s.date #fecha
                        sheet[i+3,0].number_format = 30

                        sheet[i+3,1].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.start)) #hora declarada
                        sheet[i+3,1].number_format = 41

                        sheet[i+3,2].value = s.iin
                        sheet[i+3,2].number_format = 41

                        sheet[i+3,3].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.end)) if s.end else 'No declara' # hroa declarada
                        if sheet[i+3,3].value != 'No declara':
                            sheet[i+3,3].number_format = 41

                        sheet[i+3,4].value = s.out  # salida
                        sheet[i+3,4].number_format = 41

                        sheet[i+3,5].value = 'Legada Tarde' #descripcion
                        sheet[i+3,6].value = s.iin - Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.start)) #diferencia
                        sheet[i+3,7].value = s.out - s.iin #horas trabajadas
                        sheet[i+3,8].value = s.justification.identifier if s and s.justification else ''
                        sheet[i+3,9].value = s.justification.status if s and s.justification else ''
                        i = i + 1

                    #chequeo si tiene inclumplimento
                    if s.end and s.out and s.out < Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.end)) - tolerancia:
                        sheet[i+3,0].value = s.date #fecha
                        sheet[i+3,0].number_format = 30

                        sheet[i+3,1].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.start)) #hora declarada
                        sheet[i+3,1].number_format = 41

                        sheet[i+3,2].value = s.iin
                        sheet[i+3,2].number_format = 41

                        sheet[i+3,3].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.end)) if s.end else 'No declara' # hroa declarada
                        if sheet[i+3,3].value != 'No declara':
                            sheet[i+3,3].number_format = 41

                        sheet[i+3,4].value = s.out  # salida
                        sheet[i+3,4].number_format = 41

                        sheet[i+3,5].value = 'Salida Temprana' #descripcion
                        sheet[i+3,6].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(s.end)) - s.out #diferencia
                        sheet[i+3,7].value = s.out - s.iin #horas trabajadas
                        sheet[i+3,8].value = s.justification.identifier if s and s.justification else ''
                        sheet[i+3,9].value = s.justification.status if s and s.justification else ''
                        i = i + 1

            i = i + 15


        fn = '{}.xlsx'.format(off.name)
        logging.info('salvando : {}'.format(fn))
        doc.save(fn, pyoo.FILTER_EXCEL_2007)

    finally:
        doc.close()

def findOfficeByUser(uid, offices):
    off = []
    for o in offices:
        if uid in o.users:
            off.append(o)
    return off

def findOffice(oid, offices):
    for o in offices:
        if o and o.id == oid:
            return o
    return None

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
        positions = _getPositions(con, [u.id for u in users])


        """ filtro a la gente que no debe ser manejada por el sistema de asistencia """
        usersNotInAssistance = [ uid for uid in uids if not AssistanceModel.isAssistance(con, uid, rstart, rend) ]

        """ obtengo las estadisticas """
        logging.info('Calculando las estadísticas de {} usuarios'.format(len(uids)))
        toGetStatistics = [ uid for uid in uids if uid not in usersNotInAssistance ]
        a = inject.instance(AssistanceModel)
        stats = a.getStatistics(con, toGetStatistics, rstart, rend)

        processedOffices = []
        """ creo los reportes por usuario y se lo envio """
        for user in users:

            #if user.id != '89d88b81-fbc0-48fa-badb-d32854d3d93a' and user.id != '0cd70f16-aebb-4274-bc67-a57da88ab6c7' and user.id != '4b89c515-2eba-4316-97b9-a6204d344d3a' and user.id != '35f7a8a6-d844-4d6f-b60b-aab810610809' and user.id != '205de802-2a15-4652-8fde-f23c674a1246':
            #    continue

            send = False
            rp = createReportDir(user)

            officesIds = Office.getOfficesByUserRole(con, user.id, tree=True, role='autoriza')
            ooffices = [ findOffice(oid, offices) for oid in officesIds ]
            oparents = [ o for o in ooffices if o and o.parent is None ]
            childs = {}
            for o in oparents:
                childs[o.id] = [i for i in ooffices if i and o.id == i.parent]

            ''' genero el reporte de esa oficina '''
            for parent in oparents:
                if parent.id in processedOffices:
                    continue

                processedOffices.append(parent.id)
                send = True
                statsToPyooOffice(rp, parent, childs, stats, users, positions)

            #if send:
            #    fn = createZipFile(user, rp)
            #    sendMail(con, user, fn)

    finally:
        conn.put(con)
