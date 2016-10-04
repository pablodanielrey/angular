# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../../python')

import inject
import logging
import datetime


import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config


"""
python3 persistSchedule.py sessionId userId date begin end isDayOfWeek isDayOfMonth isDayOfYear
python3 persistSchedule.py 1 35f7a8a6-d844-4d6f-b60b-aab810610809 2015-09-16 28800 54000 True False False
  35f7a8a6-d844-4d6f-b60b-aab810610809: Alejandro Oporto
"""


''' configuro el injector y el logger '''
logging.getLogger().setLevel(logging.DEBUG)


def config_injector(binder):
    binder.bind(Config, Config('server-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)

class WampMain(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)

    @coroutine
    def onJoin(self, details):
        logging.debug('********** persistSchedule **********')


        sid = sys.argv[1]
        userId = sys.argv[2]
        print(sid)
        print(userId)

        date = sys.argv[3]
        start = sys.argv[4]
        end = sys.argv[5]
        dayOfWeek = sys.argv[6]
        dayOfMonth = sys.argv[7]
        dayOfYear = sys.argv[8]

        ret = yield from self.call('assistance.persistSchedule', sid, userId, date, start, end, dayOfWeek, dayOfMonth, dayOfYear)
        logging.debug(ret)
        sys.exit()


if __name__ == '__main__':

    from autobahn.asyncio.wamp import ApplicationRunner
    from autobahn.wamp.serializer import JsonSerializer

    url = config.configs['server_url']
    realm = config.configs['server_realm']
    debug = config.configs['server_debug']

    json = JsonSerializer()
    runner = ApplicationRunner(url=url, realm=realm, debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
    runner.run(WampMain)
