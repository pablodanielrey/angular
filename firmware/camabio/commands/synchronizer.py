# -*- coding: utf-8 -*-

import sys
sys.path.append('../../../firmware/camabio')
sys.path.append('../../../python')
sys.path.append('../../../apis')

import signal, logging, threading, time
logging.getLogger().setLevel(logging.DEBUG)

from twisted.internet import task
from twisted.internet import reactor


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


url = client.network.websocket.getServerUrl()
factory = client.network.websocket.getFactory(url)


def close_sig_handler(signal,frame):
    global reactor
    reactor.stop()
    sys.exit()


if __name__ == '__main__':

    signal.signal(signal.SIGINT,close_sig_handler)

    firmware = inject.instance(Firmware)

    def syncLogs():
        firmware.syncLogs(protocol)
        reactor.connectTCP(factory.host, factory.port, factory)


    protocol.addEventHandler(firmware.syncUsersEventHandler())
    protocol.addEventHandler(firmware.syncChangedUsersEventHandler())
    protocol.addEventHandler(firmware.syncLogEventHandler())

    #synchro = Synchro(firmware)
    #synchro.start()

    t = task.LoopingCall(syncLogs)
    t.start(10)

    reactor.run()
