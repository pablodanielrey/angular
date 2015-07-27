# -*- coding: utf-8 -*-
import sys
sys.path.append('../../python')
sys.path.append('../../apis')

import logging, time, signal
import inject
import threading
import datetime

from itertools import zip_longest

import model
from model.config import Config

''' configuro el injector con las variables apropiadas '''
def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))

inject.configure(config_injector)

import camabio
from firmware import Firmware
#from network import websocket

logging.getLogger().setLevel(logging.DEBUG)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine

class WampMain(ApplicationSession):

    def __init__(self,config=None):
        logging.debug('instanciando WampMain')
        ApplicationSession.__init__(self, config)


    @coroutine
    def onJoin(self, details):
        logging.debug('session joined')

        while True:
            try:
                logging.info('identificando')
                yield from self.call('assistance.firmware.identify')

            except Exception as e:
                logging.exception(e)





'''
finalize = False

class Identifier(threading.Thread):

    def __init__(self,firmware,factory):
        super().__init__()
        self.firmware = firmware
        self.factory = factory

    def _error(self,h):
        msg = {
            'type':'ErrorEvent',
            'data':{
                'error':'La huella {} no esta asignada a ninguna persona'.format(h)
            }
        }
        emsg = self.factory._encodeMessage(msg)
        self.factory.broadcast(emsg)

    def _identified(self,log=None,user=None,sid=None,roles=None):
        msg = None
        if log:
            msg = {
                'type':'IdentifiedEvent',
                'data':{
                    'log':log,
                    'user':user,
                    'sid':sid
                }
            }
            if roles:
                msg['data']['profile'] = 'admin'

        else:
            msg = {
                'type':'IdentifiedEvent',
                'data':{
                    'msg':'No se encuentra la huella'
                }
            }
        emsg = self.factory._encodeMessage(msg)
        self.factory.broadcast(emsg)


    def run(self):
        global finalize
        while not finalize:
            try:
                logging.debug('iniciando identificación')
                self.firmware.identify(self)

            except Exception as e:
                logging.exception(e)
            finally:
                logging.debug('finalizando identificación')




def initializeNetwork():
    config = inject.instance(Config)
    log.startLogging(sys.stdout)
    factory = BroadcastServerFactory()
    factory.protocol = ActionsServerProtocol
    port = reactor.listenTCP(int(config.configs['firmware_port']), factory=factory, interface=config.configs['firmware_ip'])
    return (reactor,port,factory)





f = inject.instance(Firmware)
f.start()


try:
    (reactor,port,factory) = websocket.getPort()

    def close_sig_handler(signal,frame):
      finalize = True
      port.stopListening()
      reactor.stop()
      ' sys.exit() '

    signal.signal(signal.SIGINT,close_sig_handler)


    identifier = Identifier(f,factory)
    identifier.start()


    logging.debug('Ejecutando servidor de acciones')
    reactor.run()

    try:
        identifier.join()
    except Exception as e:
        logging.exception(e)

finally:
    f.stop()
'''

if __name__ == '__main__':


    #from autobahn.twisted.wamp import ApplicationRunner
    from autobahn.asyncio.wamp import ApplicationRunner
    from network.wampFirmware import WampFirmware

    runner = ApplicationRunner(url='ws://localhost:8000/ws',realm='assistance',debug=True, debug_wamp=True, debug_app=True)
    runner.run(WampMain)
