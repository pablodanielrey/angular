
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

from model.users.users import User, Mail


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:

        logging.info('Buscando todos los usuarios')
        uids = User.findAll(con)
        logging.info('{} usuarios encontrados'.format(len(uids)))

        logging.info('Buscando datos de usuarios')
        users = User.findById(con, [i for i,v in uids])

        t = {}
        for u in users:
            if u.type is not None:
                if u.type in t:
                    t[u.type].append(u)
                else:
                    t[u.type] = [u]

        for ty in t.keys():
            logging.info('{} = {}'.format(ty, len(t[ty])))
            with open('/tmp/{}.csv'.format(ty), 'w') as f:
                for user in t[ty]:
                    mails = Mail.findByUserId(con, user.id)
                    for mail in mails:
                        if mail.confirmed and 'econo.unlp.edu.ar' in mail.email:
                            f.write('{},{},{},{},{}\n'.format(user.id, user.dni, user.name, user.lastname, mail.email))

    finally:
        conn.put(con)
