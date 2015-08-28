# -*- coding: utf-8 -*-
import signal
import sys
import inject
import logging

# sys.path.append('../python')
sys.path.insert(0, '../python')

from model.config import Config
from model.session import Session
from model.systems.assistance.assistance import Assistance
from model.systems.offices.offices import Offices
from model.systems.assistance.justifications.LAOJustification import LAOJustification
from model.users.users import Users

import network.websocket


def config_injector(binder):
    binder.bind(Config, Config('server-config.cfg'))
    binder.bind(Session, Session())


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    inject.configure(config_injector)
    config = inject.instance(Config)

    (loop, server, factory) = network.websocket.getLoop()
    # (reactor,port,factory) = network.websocket.getPort()

    def close_sig_handler(signal, frame):
        server.close()
        loop.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    logging.debug('Ejecutando servidor de acciones')


    users = inject.instance(Users)
    assistance = inject.instance(Assistance)
    offices = inject.instance(Offices)
    laojustification = inject.instance(LAOJustification)

    con = psycopg2.connect(host="127.0.0.1", dbname="dcsys", user="dcsys", password="dcsys")

    officesList = offices.getOffices(con)
    officesId = []
    for office in officesList:
        officesId.append(office['id'])

    usersId = offices.getOfficesUsers(con,officesId)

    for userId in usersId:
        officesId.append(office['id'])
        user = users.findUser(con,userId)
        print(user)
        print(laojustification.available(None, con, userId))
