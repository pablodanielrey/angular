# -*- coding: utf-8 -*-

import sys
sys.path.append('../../../python')
sys.path.append('../../../apis')

import signal
import inject, logging
import psycopg2


from model.config import Config
from model.users.users import Users


from client.network.websocket import MyWsClientProtocol
from client.systems.assistance.firmware import Firmware

import client.network.websocket


logging.getLogger().setLevel(logging.DEBUG)

''' configuro el injector con las variables apropiadas '''
def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))

inject.configure(config_injector)
reactor = client.network.websocket.getReactor()

def close_sig_handler(signal,frame):
    global reactor
    reactor.stop()
    sys.exit()





''' en el ok del announce '''
def announceOk(protocol,message):
    global reactor
    logging.info(message)

    message['']

    users = inject.instance(Users)
    users.listUsers()



    protocol.sendClose()
    reactor.stop()


''' llamado cuando se ejecuta un open en la conexión del websocket '''
def initSync(protocol):
    logging.info('iniciando sincronización')

    firmware = inject.instance(Firmware)
    firmware.firmwareDeviceAnnounce(protocol,announceOk)






if __name__ == '__main__':

    signal.signal(signal.SIGINT,close_sig_handler)

    MyWsClientProtocol.addCallback(announce)
    reactor.run()
