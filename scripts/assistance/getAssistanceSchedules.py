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
Obtener schedules de la semana en base a un determinado dia de la semana
python3 getAssistanceSchedules.py sessionId userId date
python3 getAssistanceSchedules.py 1 35f7a8a6-d844-4d6f-b60b-aab810610809 10-10-2015

"""

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

        date = datetime.datetime.strptime(sys.argv[3], "%d-%m-%Y").date()

        from dateutil.parser import parse
        import dateutil
        tz = dateutil.tz.tzlocal()

        ret = yield from self.call('assistance.getSchedules', sid, userId, date)

        if len(ret) > 0:
            for r in ret:
                start = parse(r['start'])
                start = start.astimezone(tz)
                end = parse(r['end'])
                end = end.astimezone(tz)
                logging.debug('{} : {} --> {}'.format(r['id'], start, end))
      
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
