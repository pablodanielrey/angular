# -*- coding: utf-8 -*-
import sys
sys.path.append('../../python')

import inject
import logging
from model.config import Config

''' configuro el injector con las variables apropiadas '''


def config_injector(binder):
    binder.bind(Config, Config('firmware-config.cfg'))

inject.configure(config_injector)

import camabio
from firmware import Firmware
# from network import websocket

logging.getLogger().setLevel(logging.DEBUG)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine


class WampMain(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando wampSinchronizer')
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


if __name__ == '__main__':
    # from autobahn.twisted.wamp import ApplicationRunner
    from autobahn.asyncio.wamp import ApplicationRunner
    from network.wampFirmware import WampFirmware

    runner = ApplicationRunner(url='ws://localhost:8000/ws', realm='assistance', debug=True, debug_wamp=True, debug_app=True)
    runner.run(WampMain)
