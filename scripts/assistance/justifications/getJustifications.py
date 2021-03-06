# -*- coding: utf-8 -*-
'''
Obtener justificaciones de un usuario
@author Ivan
@example python3 getJustifications.py sid
@example python3 getJustifications.py 1
'''

import sys
sys.path.insert(0, '../../../python')

import inject
import logging
import asyncio

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
sid = sys.argv[1]




class WampMain(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        
        self.serverConfig = inject.instance(Config)

    @coroutine
    def onJoin(self, details):
        logging.debug('********** getJustifications **********')

        justifications = yield from self.call('assistance.justifications.getJustifications', sid)
        
        for just in justifications:
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
