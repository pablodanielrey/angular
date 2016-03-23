
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
from model.assistance.utils import Serializer, serializer_loads

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    try:
        con = conn.get()

        a = inject.instance(AssistanceModel)
        wps = a.getWorkPeriods(con, ['77979435-b43f-4c8b-91a9-5a84ecb46261'], datetime.datetime.now() - datetime.timedelta(365), datetime.datetime.now())

        for w in wps:
            if w.schedule is None:
                logging.info('{} día {} no tenía que venir a trabajar'.format(w.date, w.date.weekday()))

        """
        ser = json.dumps(wps, cls=Serializer)
        logging.info("\n\n\n\n")
        logging.info(ser)

        wps2 = json.loads(ser, object_hook=serializer_loads)
        logging.info("\n\n\n\n")
        logging.info(wps2)
        """

    finally:
        conn.put(con)
