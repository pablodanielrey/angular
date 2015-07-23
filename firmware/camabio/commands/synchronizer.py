# -*- coding: utf-8 -*-

import sys
sys.path.append('../../../firmware/camabio')
sys.path.append('../../../python')
sys.path.append('../../../apis')

import signal, logging, threading, time
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
protocol = client.network.websocket.getProtocol()

class Synchro(threading.Thread):

    def __init__(self,firmware):
        super().__init__()
        self.firmware = firmware


    def run(self):
        while True:
            logging.info('Sincronizando usuarios')
            self.firmware.syncUsers(protocol)

            logging.info('Sincronizando logs')
            self.firmware.syncLogs(protocol)

            time.sleep(10)



def close_sig_handler(signal,frame):
    global reactor
    reactor.stop()
    sys.exit()


if __name__ == '__main__':

    signal.signal(signal.SIGINT,close_sig_handler)

    firmware = inject.instance(Firmware)

    protocol.addEventHandler(firmware.syncUsersEventHandler())
    protocol.addEventHandler(firmware.syncChangedUsersEventHandler())
    protocol.addEventhandler(firmware.syncLogEventHandler())

    synchro = Synchro(firmware)
    synchro.start()

    reactor.run()
