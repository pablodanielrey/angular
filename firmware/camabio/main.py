import sys
sys.path.append('../../python')

import logging, time, threading, signal
import inject
import threading

from itertools import zip_longest

import model
from model.config import Config

""" configuro el injector con las variables apropiadas """
def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))

inject.configure(config_injector)

import camabio
from firmware import Firmware
from network import websocket

logging.getLogger().setLevel(logging.DEBUG)

finalize = False

class Identifier(threading.Thread):

    def __init__(self,firmware):
        super(Identifier,self).__init__()
        self.firmware = firmware

    def run(self):
        global finalize
        while not finalize:
            self.firmware.identify()



f = inject.instance(Firmware)
f.start()

identifier = Identifier(f)
identifier.start()

try:
    """ inicializo la parte de red """
    (reactor,port,factory) = websocket.getPort()

    """ inicializo el cierre del programa """
    def close_sig_handler(signal,frame):
      finalize = True
      port.stopListening()
      reactor.stop()
      sys.exit()

    signal.signal(signal.SIGINT,close_sig_handler)


    logging.debug('Ejecutando servidor de acciones')
    reactor.run()

finally:
    f.stop()
