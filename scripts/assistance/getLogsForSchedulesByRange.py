# -*- coding: utf-8 -*-
'''
Obtener schedules a partir de una rango de fechas
@author Ivan
@example python3 getLogsForSchedulesByRange.py userId date1 date2
@example python3 getLogsForSchedulesByRange.py e43e5ded-e271-4422-8e85-9f1bc0a61235 14/04/2015 15/04/2015
'''

import sys
sys.path.insert(0, '../../python')

import inject
import logging
import datetime
import dateutil


import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config
from model.systems.assistance.schedule import ScheduleData
from collections import OrderedDict




''' configuro el injector y el logger '''
#logging.getLogger().setLevel(logging.DEBUG)


def config_injector(binder):
    binder.bind(Config, Config('server-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)

sid = sys.argv[1]
userId = sys.argv[2]


class WampMain(ApplicationSession):

    def __init__(self, config=None):
        #logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)

    @coroutine
    def onJoin(self, details):
        logging.debug('********** getLogsForSchedulesByDate **********')

        userId = sys.argv[1]
        dateParamStart = sys.argv[2]
        dateParamEnd = sys.argv[3]        
        
        
        
        dateStart = datetime.datetime.strptime(dateParamStart, "%d/%m/%Y").date()
        dateEnd = datetime.datetime.strptime(dateParamEnd, "%d/%m/%Y").date()

        date = dateStart
        logsByDate = OrderedDict()
        while date != dateEnd:
          schedules = yield from self.call('assistance.getSchedulesByDate', userId, date)        
          logs = yield from self.call('assistance.getLogsForSchedulesByDate', schedules, date)
          if(len(logs)):
            logsByDate[date.strftime('%d/%m/%Y')] = logs
            
          date = date + datetime.timedelta(days=1)
          
        if(len(logsByDate)):
           print("scheduleDate, log, user_id")
        for date in logsByDate:
          for log in logsByDate[date]:
         
             print(date + ", " + log["log"] + ", " + log["userId"])
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
