# -*- coding: utf-8 -*-
import inject
import datetime
import logging
import sys
sys.path.insert(0, '../../python')

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config

"""
python3 getAssistanceData.py sessionId userId date
python3 getAssistanceData.py 1 35f7a8a6-d844-4d6f-b60b-aab810610809 10-06-2015
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
        logging.debug('***** getAssistanceData *****')
        
        sid = sys.argv[1]
        userId = sys.argv[2]
        date = datetime.datetime.strptime(sys.argv[3], "%d-%m-%Y").date()
        print(date)

        ret = yield from self.call('assistance.getAssistanceData', sid, userId, date)
        print(ret)
        
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
