
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


def createReportDir(office):
    import os
    newpath = '/tmp/reporte-asistencia-{}-{}'.format(office, datetime.datetime.now())
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

def statsToPyoo(rp, stats, users, offices):
    import uuid
    import pyoo
    calc = pyoo.Desktop('localhost', 2002)
    doc = calc.open_spreadsheet('templateStats.ods')
    try:
        sheetIndex = 0
        io = 1
        for off in offices:

            sheet = doc.sheets[0]
            sheet[io,0].value = off.name

            i = io + 2
            for uid in off.users:
                user = findUser(uid, users)
                if user:
                    status = stats[user.id][0]
                    sheet = doc.sheets[0]

                    sheet[i,0].value = user.name + " " + user.lastname
                    sheet[i,1].value = status.position if status.position is not None else ''

                    sheet[i,2].value = _secondsToHours(status.secondsToWork)
                    sheet[i,3].value = _secondsToHours(status.secondsWorked)
                    sheet[i,4].value = _secondsToHours(status.secondsLate)
                    sheet[i,5].value = status.countLate
                    sheet[i,6].value = _secondsToHours(status.secondsEarly)
                    sheet[i,7].value = status.countEarly

                    sheet[i,8].value = status.countAbsences
                    sheet[i,9].value = status.countJustificatedAbsences

                    i = i + 1

            io = i + 1


        sheetIndex = 2
        # los sheets de cada oficina
        for off in offices:

            if off is None:
                continue

            if off.name is None:
                off.name = 'Oficina {}'.format(sheetIndex)

            logging.info('Generando : {} - {}'.format(off.id, off.name))

            sheet = doc.sheets.copy('Modelo Detalle de Oficina', 'Detalle {} {}'.format(off.name, sheetIndex), sheetIndex)
            sheetIndex = sheetIndex + 1

            sheet[1,0].value = off.name
            i = 3

            for uid in sortOfficeUsers(off.users, stats):
                user = findUser(uid, users)
                if user:
                    status = stats[user.id][0]

                    for st in status.dailyStats:
                        sheet[i,0].value = user.name + " " + user.lastname
                        sheet[i,1].value = status.position if status.position is not None else ''
                        sheet[i,2].value = st.date
                        sheet[i,3].value = st.start if st.start is not None else ''
                        sheet[i,4].value = st.end if st.end is not None else ''
                        sheet[i,5].value = _secondsToHours(st.periodSeconds) if st.periodSeconds > 60 else ''
                        sheet[i,6].value = st.iin if st.iin is not None else ''

                        if not st.isBoss:
                            sheet[i,7].value = st.out if st.out is not None else ''
                            sheet[i,8].value = _secondsToHours(st.workedSeconds) if st.workedSeconds > 60 else ''

                            if st.workedSeconds > 0:
                                aditional = int(st.workedSeconds - st.periodSeconds)
                                if aditional > 60:
                                    sheet[i,9].value = '+{}'.format(_secondsToHours(aditional))
                                    sheet[i,9].text_color = 0x669900
                                elif aditional < 60:
                                    aditional = aditional * -1
                                    sheet[i,9].value = '-{}'.format(_secondsToHours(aditional))
                                    if aditional > (30 * 60):
                                        sheet[i,9].text_color = 0xffffff
                                        sheet[i,9].background_color = 0xcc3300
                                    else:
                                        sheet[i,9].text_color = 0xcc3300

                        sheet[i,10].value = st.justification.identifier if st.justification is not None else ''
                        sheet[i,11].value = _secondsToHours(st.justification.seconds) if st.justification is not None else ''
                        if st.justification is not None:
                            if st.justification.status == 1:
                                sheet[i,12].value = 'P'
                                sheet[i,12].text_color = 0xffffff
                                sheet[i,12].background_color = 0x0000cc

                            elif st.justification.status == 2:
                                sheet[i,12].value = 'A'
                                sheet[i,12].text_color = 0xffffff
                                sheet[i,12].background_color = 0x669900
                                sheet[i,10].text_color = 0xffffff
                                sheet[i,10].background_color = 0x669900
                                sheet[i,11].text_color = 0xffffff
                                sheet[i,11].background_color = 0x669900

                            elif st.justification.status == 3:
                                sheet[i,12].value = 'R'
                                sheet[i,12].text_color = 0xffffff
                                sheet[i,12].background_color = 0xcc3300

                            elif st.justification.status == 4:
                                sheet[i,12].value = 'C'

                        if st.isAbsence() and not st.isJustificatedAbsence():
                            sheet[i,13].value = 'A'
                            sheet[i,13].text_color = 0xffffff
                            sheet[i,13].background_color = 0xcc3300

                        elif not st.isBoss and (st.start is not None and st.end is not None) and (st.iin is None or st.out is None) and (st.justification is None):
                            sheet[i,13].value = 'M'
                            sheet[i,13].text_color = 0xffffff
                            sheet[i,13].background_color = 0xcc3300

                        i = i + 1

            #index = index + 1
        f = str(uuid.uuid4())
        fn = '{}/assistencia-{}.xlsx'.format(rp, offices[0].name)
        logging.info('salvando : {}'.format(fn))
        doc.save(fn, pyoo.FILTER_EXCEL_2007)

    finally:
        doc.close()

def createZipFile(rp):
    import zipfile
    import os
    fn = '/tmp/reporte-asistencia.zip'
    with zipfile.ZipFile(fn, mode='w', compression=zipfile.ZIP_BZIP2) as rpzip:
        for root, dir, files in os.walk(rp):
            for f in files:
                fm = '{}/{}'.format(root, f)
                logging.info('escribiendo : {}'.format(fm))
                rpzip.write(fm)
    logging.info('generado : {}'.format(fn))


def _getOffices(con):
    return Office.findById(con, Office.findAll(con))

def _getUsers(con):
    uids = []

    """
    uid, v = UserDAO.findByDni(con, "26575940")
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "18854479")
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "26106065")
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "24040623")
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "32393755")    # pablo Lozada
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "27528150")    # julio ciappa
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "18609353")    # juan acosta
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "24040623")     # miguel rey
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "27821597")     # maxi
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "31073351")     # ivan
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "33212183")     # santiago
    uids.append(uid)

    #uid, v = UserDAO.findByDni(con, "27294557")     # pablo
    #uids.append(uid)

    uid, v = UserDAO.findByDni(con, "30001823")    # walter
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "31381082")     # ema
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "29694757")      # oporto
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "30078613")      # lorena mabel pereira
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "30078613")      # lorena mabel pereira
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "21430694")      # analía causa
    uids.append(uid)

    """
    uids = ScheduleDAO.findUsersWithSchedule(con)
    users = UserDAO.findById(con, uids)
    return users, uids


def findUser(uid, users):
    for u in users:
        if u.id == uid:
            return u
    return None



if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    rstart = datetime.datetime.now() - datetime.timedelta(days=7)
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

        users, userIds = _getUsers(con)

        a = inject.instance(AssistanceModel)
        stats = a.getStatistics(con, userIds, rstart, rend)

        for office in offices:
            rp = createReportDir()
            statsToPyoo(rp, stats, users, [office])
            createZipFile(office, rp)

    finally:
        conn.put(con)
