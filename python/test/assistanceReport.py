
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

class WpStatistics:

    def __init__(self, userId):
        self.userId = userId
        self.secondsToWork = 0              # total que deberia trabajar
        self.secondsWorked = 0              # total trabajado
        self.secondsLate = 0                # total de llegadas tarde
        self.countLate = 0                  # cantidad de llegadas tarde
        self.secondsEarly = 0               # total de salidas tempranas
        self.countEarly = 0                 # cantidad de salidas tempranas

    def updateStatistic(self, start, end, hourStart, hourEnd):

        if end is not None and start is not None:
            self.secondsToWork = self.secondsToWork + (end - start).total_seconds()

        if hourStart is not None and hourEnd is not None:
            self.secondsWorked = self.secondsWorked + (hourEnd - hourStart).total_seconds()

        if hourStart is not None and start is not None and hourStart > start:
            self.secondsLate = self.secondsLate + (hourStart - start).total_seconds()
            self.countLate = self.countLate + 1

        if hourEnd is not None and end is not None and end > hourEnd:
            self.secondsEarly = self.secondsEarly + (end - hourEnd).total_seconds()
            self.countEarly = self.countEarly + 1


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
                stats = WpStatistics(user.id)

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

                    stats.updateStatistic(sd, ed, hi, hs)
                    index = index + 1


                """ calculo los totales """
                indexLastData = index
                index = index + 4
                #sheet[index-1,6].value = 'Cantidad Total a Trabajar'
                sheet[index,6].value = stats.secondsToWork
                sheet[index+1,6].value = '{} d {} h {} m {} s'.format(int(stats.secondsToWork / 60 / 60 / 24), int(stats.secondsToWork / 60 / 60), int(stats.secondsToWork / 60 % 60), int(stats.secondsToWork % 60))

                #index = index + 4
                #sheet[index-1,6].value = 'Cantidad Total Trabajada'
                sheet[index,9].value = stats.secondsWorked
                sheet[index+1,9].value = '{} d {} h {} m {} s'.format(int(stats.secondsWorked / 60 / 60 / 24), int(stats.secondsWorked / 60 / 60), int(stats.secondsWorked / 60 % 60), int(stats.secondsWorked % 60))

                #index = index + 4
                #sheet[index-1,6].value = 'Cantidad Total de Lllegadas Tarde'
                sheet[index,50].value = int(stats.secondsLate)
                #sheet[index+1,10].value = '{} d {} h {} m {} s'.format(int(stats.secondsLate / 60 / 60 / 24), int(stats.secondsLate / 60 / 60), int(stats.secondsLate / 60 % 60), int(stats.secondsLate % 60))
                sheet[index,10].value = '{} llegadas tarde'.format(int(stats.countLate))

                #index = index + 4
                #sheet[index-1,6].value = 'Cantidad Total de Salidas Tempranas'
                sheet[index,51].value = int(stats.secondsEarly)
                #sheet[index+1,11].value = '{} d {} h {} m {} s'.format(int(stats.secondsEarly / 60 / 60 / 24), int(stats.secondsEarly / 60 / 60), int(stats.secondsEarly / 60 % 60), int(stats.secondsEarly % 60))
                sheet[index,11].value = '{} Salidas Tempranas'.format(int(stats.countEarly))


                """ armo los graficos comparativos """

                chartSize = 10
                chartLength = int(len(wp) / 4)
                columnStart = 3

                # horas de trabajo / horas trabajadas
                chartStart = indexLastData + 10;
                chartEnd = chartStart + chartSize
                sheet[chartStart,0].value = 'Trabajo/Trabajadas'
                c = sheet.charts.create('{}'.format(user.id), sheet[chartStart:chartEnd, columnStart:columnStart + chartLength], [sheet[2:indexLastData, 6:7], sheet[2:indexLastData, 9:10]])

                # horas trabajadas / llegadas tarde
                chartStart = chartEnd + 1
                chartEnd = chartStart + chartSize
                sheet[chartStart,0].value = 'Trabajadas/Llegadas Tarde'
                c2 = sheet.charts.create('{} 2'.format(user.id), sheet[chartStart:chartEnd, columnStart:columnStart + chartLength], [sheet[2:indexLastData, 9:10], sheet[2:indexLastData, 10:11]])

                # horas trabajadas / salidas temprano
                chartStart = chartEnd + 1
                chartEnd = chartStart + chartSize
                sheet[chartStart,0].value = 'Trabajadas/Salidas Temprano'
                c3 = sheet.charts.create('{} 3'.format(user.id), sheet[chartStart:chartEnd, columnStart:columnStart + chartLength], [sheet[2:indexLastData, 9:10], sheet[2:indexLastData, 11:12]])

                chartLength = 2
                indexData = indexLastData + 4
                # total horas trabajadas / total horas llegadas tarde
                chartStart = chartEnd + 1
                chartEnd = chartStart + chartSize
                sheet[chartStart,0].value = 'Total: Trabajadas/Llegadas Tarde'
                c3 = sheet.charts.create('{} 4'.format(user.id), sheet[chartStart:chartEnd, columnStart:columnStart + chartLength], [sheet[indexData, 9], sheet[indexData, 50]])

                # total horas trabajadas / total horas de salidas temprano
                chartStart = chartEnd + 1
                chartEnd = chartStart + chartSize
                sheet[chartStart,0].value = 'Total: Trabajadas/Salidas Temprano'
                c3 = sheet.charts.create('{} 5'.format(user.id), sheet[chartStart:chartEnd, columnStart:columnStart + chartLength], [sheet[indexData, 9], sheet[indexData, 51]])


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

    uid, v = UserDAO.findByDni(con, "27821597")     # maxi
    uids.append(uid)

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
