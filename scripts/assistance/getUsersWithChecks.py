# -*- coding: utf-8 -*-
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

class WampMain(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)

    @coroutine
    def onJoin(self, details):
        logging.debug('ejecutando llamadas')

        date = datetime.datetime.strptime(sys.argv[2], "%d-%m-%Y")
        logging.debug('consutlando {}'.format(date))
        # date = parse(sys.argv[3], dayfirst=True, yearfirst=False)
        tz = dateutil.tz.tzlocal()

        ret = yield from self.call('assistance.getUsersWithChecks', sid, date)
        for r in ret:
            user = yield from self.call('users.findById', r)
            logging.debug(user)

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
