# -*- coding: utf-8 -*-
import sys
sys.path.append('../../python')
sys.path.append('../../apis')

import logging, time, threading, signal
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



if __name__ == '__main__':


    #from autobahn.twisted.wamp import ApplicationRunner
    from autobahn.asyncio.wamp import ApplicationRunner
    from network.wampFirmware import WampFirmware

    runner = ApplicationRunner(url='ws://localhost:8000/ws',realm='assistance',debug=False, debug_wamp=True, debug_app=False)
    runner.run(WampFirmware)
