# -*- coding: utf-8 -*-
'''
Obtener justificaciones de un usuario
@author Ivan
@example python3 updateJustificationStockByUser.py userId justificationId stock
@example python3 updateJustificationStockByUser.py 35f7a8a6-d844-4d6f-b60b-aab810610809 48773fd7-8502-4079-8ad5-963618abe725 15
@note 35f7a8a6-d844-4d6f-b60b-aab810610809 (ivan)
@note 48773fd7-8502-4079-8ad5-963618abe725 (compensatorio)
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






class WampMain(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        
        self.serverConfig = inject.instance(Config)

    @coroutine
    def onJoin(self, details):
        logging.debug('********** updateJustificationsStockByUser **********')

        ###### parametros #####
        userId = sys.argv[1]
        justificationId = sys.argv[2]
        stock = sys.argv[3]

        
        yield from self.call('assistance.justifications.updateJustificationStock', 1, userId, justificationId, stock)



            
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
