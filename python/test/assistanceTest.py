
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

from model.serializer.utils import MySerializer, serializer_loads

from model.users.users import UserDAO

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    try:
        con = conn.get()

        logging.info('buscando los usuarios')

        uid, v = UserDAO.findByDni(con, sys.argv[1])
        uids = [uid]
        # uids = [ u for u,v in UserDAO.findAll(con) ]

        logging.info('cargando los periodos')

        a = inject.instance(AssistanceModel)
        wps = a.getWorkPeriods(con, uids, datetime.datetime.now() - datetime.timedelta(10000), datetime.datetime.now())

        logs = []
        for w in wps:
            wp = wps[w]
            for w1 in wp:
                sec = w1.getWorkedSeconds()
                logging.info('{} --> e:{}, s:{} --> {}:{} '.format(w1.date, w1.getStartDate(), w1.getEndDate(), int(sec / 60 / 60), int(sec / 60 % 60)))

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
        j.owner = uid
        j.start = datetime.date.today()
        j.number = 65905
        j.persist(con, 30)
        logging.info(j)
        con.commit()

    finally:
        conn.put(con)
