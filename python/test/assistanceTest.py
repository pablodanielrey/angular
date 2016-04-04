
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
        #uid, v = UserDAO.findByDni(con, "30001823")    # walter
        #uid, v = UserDAO.findByDni(con, "27821597")     # maxi
        #uid, v = UserDAO.findByDni(con, "31073351")     # ivan
        #uid, v = UserDAO.findByDni(con, "33212183")     # santiago
        #uid, v = UserDAO.findByDni(con, "27294557")     # pablo
        #uid, v = UserDAO.findByDni(con, "31381082")     # ema
        #uid, v = UserDAO.findByDni(con, "29694757")      # oporto
        uids.append(uid)

        #uid, v = UserDAO.findByDni(con, "31381082")
        #uids.append(uid)

        #uids = [ u for u,v in UserDAO.findAll(con) ]

        logging.info('cargando los periodos')

        a = inject.instance(AssistanceModel)
        wps = a.getWorkPeriods(con, uids, datetime.datetime.now() - datetime.timedelta(days=63), datetime.datetime.now())

        totalHoras = 0
        logs = []
        for w in wps:
            wp = wps[w]
            for w1 in wp:
                sec = w1.getWorkedSeconds()
                hi = None if w1.getStartLog() is None else w1.getStartLog().log.time()
                hs = None if w1.getEndLog() is None else w1.getEndLog().log.time()
                logging.info('{} --> e:{}, s:{} --> {}:{} -- he {} - hs {}'.format(w1.date, w1.getStartDate(), w1.getEndDate(), int(sec / 60 / 60), int(sec / 60 % 60), hi, hs))
                totalHoras = totalHoras + sec

        logging.info('total de horas trabajadas : {}:{}'.format(int(totalHoras / 60 / 60), int(totalHoras / 60 % 60)))

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
