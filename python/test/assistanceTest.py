
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

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)

    conn = Connection(reg.getRegistry('dcsys'))
    try:
        con = conn.get()

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
        doc = calc.open_spreadsheet('/tmp/prueba.ods')
        sheet = doc.sheets[0]

        index = 2
        totalHoras = 0
        logs = []
        for w in wps:
            wp = wps[w]
            for w1 in wp:
                sec = w1.getWorkedSeconds()
                sd = w1.getStartDate()
                ed = w1.getEndDate()
                hi = None if w1.getStartLog() is None else w1.getStartLog().log.time()
                hs = None if w1.getEndLog() is None else w1.getEndLog().log.time()
                th = int(sec / 60 / 60)
                tm = int(sec / 60 % 60)
                logging.info('{} --> e:{}, s:{} --> {}:{} -- he {} - hs {}'.format(w1.date, sd, ed, th, tm, hi, hs))
                totalHoras = totalHoras + sec

                sheet[index,0].value = w1.date
                sheet[index,1].value = sd
                sheet[index,2].value = ed
                sheet[index,3].value = hi
                sheet[index,4].value = hs
                sheet[index,5].value = sec
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

        '''
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
        '''
    finally:
        conn.put(con)
