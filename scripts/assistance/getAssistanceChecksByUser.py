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

''' configuro el injector y el logger '''
logging.getLogger().setLevel(logging.DEBUG)


def config_injector(binder):
    binder.bind(Config, Config('server-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)

sid = sys.argv[1]
userId = sys.argv[2]


class WampMain(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)

    @coroutine
    def onJoin(self, details):
        logging.debug('ejecutando llamadas')

        date = datetime.datetime.now()

        from dateutil.parser import parse
        import dateutil
        tz = dateutil.tz.tzlocal()

        days = 20
        c = 0
        while c < days:
            ret = yield from self.call('assistance.getChecksByUser', sid, userId, date)

            if len(ret) > 0:
                for r in ret:
                    start = parse(r['start'])
                    start = start.astimezone(tz)
                    end = parse(r['end'])
                    end = end.astimezone(tz)
                    logging.debug('{} : {} --> {}'.format(r['id'], start, end))
            c = c + 1
            date = date + datetime.timedelta(days=1)

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
