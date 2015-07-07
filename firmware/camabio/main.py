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

    def __init__(self,firmware,factory):
        super(Identifier,self).__init__()
        self.firmware = firmware
        self.factory = factory

    def _error(self,h):
        self.factory.broadcast('huella {} no asignada a persona'.format(h))

    def _identified(self,log):
        self.factory.broadcast(log)


    def run(self):
        global finalize
        while not finalize:
            try:
                logging.debug('iniciando identificación')
                self.firmware.identify()
            except Exception as e:
                logging.critical(e)
            finally:
                logging.debug('finalizando identificación')


f = inject.instance(Firmware)
f.start()


try:
    """ inicializo la parte de red """
    (reactor,port,factory) = websocket.getPort()

    """ inicializo el cierre del programa """
    def close_sig_handler(signal,frame):
      finalize = True
      port.stopListening()
      reactor.stop()
      ' sys.exit() '

    signal.signal(signal.SIGINT,close_sig_handler)


    ''' inicializo el tema del identificador '''
    identifier = Identifier(f,factory)
    identifier.start()


    logging.debug('Ejecutando servidor de acciones')
    reactor.run()

    try:
        identifier.join()
    except Exception as e:
        logging.critical(e)

finally:
    f.stop()
