import sys
sys.path.append('../../python')

import logging, time, threading, signal
import inject

from itertools import zip_longest
import camabio

import model
from model.config import Config

from firmware import FirmwareReader, Firmware
from network import websocket

logging.getLogger().setLevel(logging.DEBUG)

""" configuro el injector con las variables apropiadas """
def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))

inject.configure(config_injector)

f = inject.instance(Firmare)
f.start()
try:
    """ inicializo la parte de red """
    (reactor,port,factory) = websocket.getPort()

    """ inicializo el cierre del programa """
    def close_sig_handler(signal,frame):
      port.stopListening()
      reactor.stop()
      sys.exit()

    signal.signal(signal.SIGINT,close_sig_handler)


    logging.debug('Ejecutando servidor de acciones')
    reactor.run()

finally:
    f.stop()
