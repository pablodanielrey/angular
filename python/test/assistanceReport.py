
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
from model.assistance.assistance import AssistanceModel
from model.assistance.justifications.shortDurationJustification import ShortDurationJustification
from model.assistance.justifications.longDurationJustification import LongDurationJustification
from model.assistance.justifications.status import Status
from model.assistance.justifications.justifications import Justification
from model.assistance.schedules import ScheduleDAO

from model.serializer.utils import MySerializer, serializer_loads

from model.users.users import UserDAO

def findUser(users, uid):
    for u in users:
        if uid == u.id:
            return u

def workedPeriodsToPyoo(wps, users):

    import uuid
    f = str(uuid.uuid4())
    fn = '/tmp/{}.ods'.format(f)

    import pyoo
    calc = pyoo.Desktop('localhost', 2002)
    doc = calc.open_spreadsheet('template.ods')
    try:
        sheetIndex = 0

        for user in users:

            if user:

                """ creo una copia del template para poder llenar los datos """
                sheet = doc.sheets.copy('Template', '{} {} {}'.format(user.dni, user.name, user.lastname), sheetIndex)
                sheetIndex = sheetIndex + 1

                index = 2
                wp = wps[user.id]
                for w1 in wp:
                    sec = w1.getWorkedSeconds()
                    sd = w1.getStartDate()
                    ed = w1.getEndDate()
                    hi = None if w1.getStartLog() is None else w1.getStartLog().log.astimezone(tzlocal()).replace(tzinfo=None)
                    hs = None if w1.getEndLog() is None else w1.getEndLog().log.astimezone(tzlocal()).replace(tzinfo=None)

                    sheet[index,0].value = user.dni
                    sheet[index,1].value = user.name
                    sheet[index,2].value = user.lastname

                    sheet[index,3].value = w1.date
                    if sd is not None: sheet[index,4].value = sd
                    if ed is not None: sheet[index,5].value = ed
                    if sd is not None and ed is not None: sheet[index,6].formula = '={}-{}'.format(sheet[index,5].address, sheet[index,4].address)

                    if hi is not None: sheet[index,7].value = hi
                    if hs is not None: sheet[index,8].value = hs

                    if hi is not None and hs is not None:
                        sheet[index,9].formula = '={}-{}'.format(sheet[index,8].address, sheet[index,7].address)

                    if hi is not None and hi > sd:
                        sheet[index,10].formula = '={}-{}'.format(sheet[index,7].address, sheet[index,4].address)
                    #else:
                        #sheet[index,9].value = 0

                    if hs is not None and ed > hs:
                        sheet[index,11].formula = '={}-{}'.format(sheet[index,5].address, sheet[index,8].address)
                    #else:
                        #sheet[index,10].value = 0

                    if len(w1.justifications) > 0:
                        sheet[index,12].value = w1.justifications[0].getIdentifier()

                    index = index + 1



            #c = sheet.charts.create('Horas Trabajadas {}'.format(len(sheet.charts)), sheet[chartStart:index, 12:12 + len(wp)], sheet[chartStart:index, 9:10])
            #index = index + 1
        doc.save(fn)

    finally:
        doc.close()


def _getUsers(con):
    uids = []

    #uid, v = UserDAO.findByDni(con, "32393755")    # pablo Lozada
    #uids.append(uid)

    #uid, v = UserDAO.findByDni(con, "27528150")    # julio ciappa
    #uids.append(uid)

    #uid, v = UserDAO.findByDni(con, "18609353")    # juan acosta
    #uids.append(uid)

    #uid, v = UserDAO.findByDni(con, "24040623")     # miguel rey
    #uids.append(uid)

    #uid, v = UserDAO.findByDni(con, "27821597")     # maxi
    #uids.append(uid)

    uid, v = UserDAO.findByDni(con, "31073351")     # ivan
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "33212183")     # santiago
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "27294557")     # pablo
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "30001823")    # walter
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "31381082")     # ema
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "29694757")      # oporto
    uids.append(uid)

    #uids = ScheduleDAO.findUsersWithSchedule(con)
    users = UserDAO.findById(con, uids)
    return users, uids


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)

    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        users, userIds = _getUsers(con)
        a = inject.instance(AssistanceModel)
        wps = a.getWorkPeriods(con, userIds, datetime.datetime.now() - datetime.timedelta(days=97), datetime.datetime.now())
        workedPeriodsToPyoo(wps, users)

    finally:
        conn.put(con)
