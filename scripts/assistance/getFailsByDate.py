# -*- coding: utf-8 -*-
"""
Obtener fallas en un intervalo de fechas
@example python3 getFailsByDate.py uid user_id date1 date2
@example python3 getFailsByDate.py 1 c3f23c7c-4abf-402e-b6f3-ee3fd70f4484 01/01/2015 01/05/2015
"""

import sys
sys.path.insert(0, '../../python')

import inject
import logging
import datetime

import dateutil
from dateutil.parser import parse


import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config

''' configuro el injector y el logger '''
logging.getLogger().setLevel(logging.DEBUG)


def config_injector(binder):
    binder.bind(Config, Config('server-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)

sid = sys.argv[1]
userId = sys.argv[2]
start = datetime.datetime.strptime(sys.argv[3], "%d/%m/%Y").date()
end = datetime.datetime.strptime(sys.argv[4], "%d/%m/%Y").date()



class WampMain(ApplicationSession):

    def __init__(self, config=None):

        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)

    @coroutine
    def onJoin(self, details):
        logging.debug('********** getFailsByDate **********')
       
        ret = yield from self.call('assistance.getFailsByDate', sid, userId, start, end)
        print(len(ret))
        for r in ret:
            logging.debug(r)

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
