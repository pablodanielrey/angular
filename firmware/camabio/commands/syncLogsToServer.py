# -*- coding: utf-8 -*-

import sys
sys.path.append('../../../firmware/camabio')
sys.path.append('../../../python')
sys.path.append('../../../apis')

import signal, logging
logging.getLogger().setLevel(logging.DEBUG)

import inject
from model.config import Config

''' configuro el injector con las variables apropiadas '''
def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))

inject.configure(config_injector)


import client.network.websocket
from firmware import Firmware

reactor = client.network.websocket.getReactor()

def close_sig_handler(signal,frame):
    global reactor
    reactor.stop()
    sys.exit()


if __name__ == '__main__':

    signal.signal(signal.SIGINT,close_sig_handler)

    client.network.websocket.connectClient()

    firmware = inject.instance(Firmware)
    firmware.syncLogs()

    reactor.run()
