# -*- coding: utf-8 -*-
'''
Obtener schedules a partir de una fecha
@author Ivan
@example python3 getSchedulesByDate.py userId date
@example python3 getSchedulesByDate.py e43e5ded-e271-4422-8e85-9f1bc0a61235 "14/04/2015"
'''

import sys
sys.path.insert(0, '../../python')

import inject
import logging
import datetime


import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config
from model.systems.assistance.schedule import ScheduleData



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
        logging.debug('********** getSchedulesByDate **********')

        userId = sys.argv[1]
        dateParam = sys.argv[2]
        
        date = datetime.datetime.strptime(dateParam, "%d/%m/%Y").date()
        
        schedulesAux = yield from self.call('assistance.getSchedulesByDate', userId, date)

        schedules = []

        for schedule in schedulesAux:
            schData = ScheduleData(schedule)
            schedules.append(schData);
            
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
