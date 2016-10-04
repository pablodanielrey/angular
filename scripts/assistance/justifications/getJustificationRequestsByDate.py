# -*- coding: utf-8 -*-
'''
Obtener justificaciones de un usuario
@author Ivan
@example python3 getJustificationRequestsByDate.py start end status user1 user2 user3
@example python3 getJustificationRequestsByDate.py "01/05/2015 10:00:00" "01/05/2015 15:00:00" APPROVED 35f7a8a6-d844-4d6f-b60b-aab810610809
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
    
        logging.debug('********** getJustificationRequestsByDate **********')
                        
        ###### parametros #####
        if len(sys.argv) < 5:
            sys.exit("Error de parametros")
        
        startParam = sys.argv[1]
        endParam = sys.argv[2]
        statusList = [sys.argv[3]]
        userIds = sys.argv[4:]

        start = datetime.datetime.strptime(startParam, "%d/%m/%Y %H:%M:%S")
        end = datetime.datetime.strptime(endParam, "%d/%m/%Y %H:%M:%S")
        
        
        ###### obtencion de datos del servidor ###### 
        justificationRequests = yield from self.call('assistance.justifications.getJustificationRequestsByDate', 1, userIds, start, end, statusList)
        for just in justificationRequests:
           print(just)
                 
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
