
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
from model.assistance.justifications.status import Status
from model.assistance.justifications.justifications import Justification

from model.serializer.utils import MySerializer, serializer_loads

from model.users.users import UserDAO

def findUser(users, uid):
    for u in users:
        if uid == u.id:
            return u

def testFindJustification(con):
        # fechas a testear
        start = datetime.datetime.now() - datetime.timedelta(days=10)
        end = datetime.datetime.now() + datetime.timedelta(days=10)

        uid, v = UserDAO.findByDni(con, "31381082")
        # creo justificaciones con lasdifrerentes opciones posibles

        # (jstart < start) and (jend >= start and jend <= end)
        j = ShortDurationJustification()
        j.userId = uid
        j.ownerId = uid
        j.start = start - datetime.timedelta(days=5)
        j.number = 70000
        j.persist(con, 10)
        con.commit()

        # (jend > end) and (jstart >= start and jstart <= end)
        j = ShortDurationJustification()
        j.userId = uid
        j.ownerId = uid
        j.start = start + datetime.timedelta(days=10)
        j.number = 70000
        j.persist(con, 15)
        con.commit()

        # se encuentra entre el start y el end
        j = ShortDurationJustification()
        j.userId = uid
        j.ownerId = uid
        j.start = start + datetime.timedelta(days=5)
        j.number = 70000
        j.persist(con, 5)
        con.commit()

        # jstart < start and jend > end
        j = ShortDurationJustification()
        j.userId = uid
        j.ownerId = uid
        j.start = start - datetime.timedelta(days=5)
        j.number = 70000
        j.persist(con, 30)
        con.commit()

        # obtengo las justificaciones

        js = Justification.getJustifications(con, uid, start, end)
        for j in js:
            j.getLastStatus(con)
            logging.info(j.__dict__)


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)

    conn = Connection(reg.getRegistry('dcsys'))
    try:
        con = conn.get()

        testFindJustification(con)
        exit(1)

        logging.info('buscando los usuarios')

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
        logging.info(uids)
        logging.info(users)


        #uid, v = UserDAO.findByDni(con, "31381082")
        #uids.append(uid)

        #uids = [ u for u,v in UserDAO.findAll(con) ]

        logging.info('cargando los periodos')

        a = inject.instance(AssistanceModel)
        wps = a.getWorkPeriods(con, uids, datetime.datetime.now() - datetime.timedelta(days=63), datetime.datetime.now())

        import uuid
        f = str(uuid.uuid4())
        fn = '/tmp/{}.ods'.format(f)

        import pyoo
        calc = pyoo.Desktop('localhost', 2002)
        doc = calc.open_spreadsheet('template.ods')
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
        doc.close()

        #logging.info(json.dumps(logs, cls=Serializer))
            #logging.info(json.dumps(wps[w], cls=Serializer))


        """
        ser = json.dumps(wps, cls=Serializer)
        logging.info("\n\n\n\n")
        logging.info(ser)

        wps2 = json.loads(ser, object_hook=serializer_loads)
        logging.info("\n\n\n\n")
        logging.info(wps2)
        """


        j = ShortDurationJustification()
        j.userId = uid
        j.ownerId = uid
        j.start = datetime.date.today()
        j.number = 65905
        j.persist(con, 30)
        con.commit()
        logging.info(j.__dict__)

        j.changeStatus(con, Status.REJECTED, uid)
        con.commit()
        logging.info(j.__dict__)



    finally:
        conn.put(con)
