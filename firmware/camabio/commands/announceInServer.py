# -*- coding: utf-8 -*-

import sys
sys.path.append('../../python')
sys.path.append('../../apis')

import inject, logging
import psycopg2


from model.config import Config
from client.network.websocket import WsClientProtocol
from client.systems.assistance.firmware import Firmware

import client.network.websocket


logging.getLogger().setLevel(logging.INFO)

""" configuro el injector con las variables apropiadas """
def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))

inject.configure(config_injector)


def announceOk():
    logging.info('Anuncio correctamente transmitido')

def announce():
    protocols = WsClientProtocol.protocols
    if len(protocols) > 0:
        protocol = WsClientProtocol.protocols[0]
        firmware = inject.instance(Firmware)
        firmware.firmwareDeviceAnnounce(protocol,announceOk)



if __name__ == '__main__':

    reactor = client.network.websocket.getReactor()
    reactor.callWhenRunning(announce)
    reactor.run()
