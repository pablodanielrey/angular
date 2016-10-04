# -*- coding: utf-8 -*-
'''
Obtener justificaciones de un usuario
@author Ivan
@example python3 getJustificationsStockByUser.py userId justificationId date
@example python3 getJustificationsStockByUser.py e43e5ded-e271-4422-8e85-9f1bc0a61235 fa64fdbd-31b0-42ab-af83-818b3cbecf46 01/05/2015
'''

import sys
sys.path.insert(0, '../../../python')

import inject
import logging
import asyncio
import datetime

from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.config import Config



###### configuracion #####
logging.getLogger().setLevel(logging.DEBUG)


def config_injector(binder):
    binder.bind(Config, Config('server-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)



###### parametros #####
userId = sys.argv[1]
justificationId = sys.argv[2]
dateParam = sys.argv[3]



class WampMain(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        
        self.serverConfig = inject.instance(Config)

    @coroutine
    def onJoin(self, details):
        logging.debug('********** getJustificationsStockByUser **********')

        date = datetime.datetime.strptime(dateParam, "%d/%m/%Y %H:%M:%S")
        
        justificationsStock = yield from self.call('assistance.justifications.getJustificationsStockByUser', 1, userId, justificationId, date, None)
        print(justificationsStock)


            
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
