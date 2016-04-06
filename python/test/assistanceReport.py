
import json
import datetime
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

from model.serializer.utils import MySerializer, serializer_loads

from model.users.users import UserDAO

def findUser(users, uid):
    for u in users:
        if uid == u.id:
            return u


def workedPeriodsToPyoo(wps):
    import uuid
    f = str(uuid.uuid4())
    fn = '/tmp/{}.ods'.format(f)

    import pyoo
    calc = pyoo.Desktop('localhost', 2002)
    doc = calc.open_spreadsheet('template.ods')
    try:
        sheet = doc.sheets[0]

        sh = 0
        chartStart = 0
        index = 2
        totalHoras = 0
        logs = []
        for w in wps:
            chartStart = index
            wp = wps[w]
            for w1 in wp:
                sec = w1.getWorkedSeconds()
                sd = '' if w1.getStartDate() is None else w1.getStartDate()
                ed = '' if w1.getEndDate() is None else w1.getEndDate()
                hi = '' if w1.getStartLog() is None else w1.getStartLog().log.time()
                hs = '' if w1.getEndLog() is None else w1.getEndLog().log.time()
                th = int(sec / 60 / 60)
                tm = int(sec / 60 % 60)
                logging.info('{} --> e:{}, s:{} --> {}:{} -- he {} - hs {}'.format(w1.date, sd, ed, th, tm, hi, hs))
                totalHoras = totalHoras + sec

                us = findUser(users, w1.userId) if findUser(users, w1.userId) is not None else 'nada'
                sheet[index,0].value = us.dni if us != 'nada' else ''
                sheet[index,1].value = us.name if us != 'nada' else ''
                sheet[index,2].value = us.lastname if us != 'nada' else ''
                sheet[index,3].value = w1.date
                sheet[index,4].value = sd
                sheet[index,5].value = ed
                sheet[index,6].value = hi
                sheet[index,7].value = hs
                #sheet[index,8].value = datetime.timedelta(seconds=sec)
                sheet[index,8].value = sec
                sheet[index,9].formula = '={}/60/60'.format(sheet[index,8].address)
                index = index + 1

            logging.info(chartStart)
            logging.info(index)
            c = sheet.charts.create('Horas Trabajadas {}'.format(len(sheet.charts)), sheet[chartStart:index, 12:12 + len(wp)], sheet[chartStart:index, 9:10])
            #c.change_type(pyoo.LineDiagram)
            index = index + 1

        logging.info('total de horas trabajadas : {}:{}'.format(int(totalHoras / 60 / 60), int(totalHoras / 60 % 60)))

        doc.save(fn)
        
    finally:
        doc.close()


def _getUsers(con):
    uids = []

    uid, v = UserDAO.findByDni(con, "30001823")    # walter
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "27821597")     # maxi
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "31073351")     # ivan
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "33212183")     # santiago
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "27294557")     # pablo
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "31381082")     # ema
    uids.append(uid)

    uid, v = UserDAO.findByDni(con, "29694757")      # oporto
    uids.append(uid)

    users = UserDAO.findById(con, uids)
    return users


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)

    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        users = _getUsers(con)
        a = inject.instance(AssistanceModel)
        wps = a.getWorkPeriods(con, uids, datetime.datetime.now() - datetime.timedelta(days=63), datetime.datetime.now())



        workedPeriodsToPyoo(wps)

    finally:
        conn.put(con)
