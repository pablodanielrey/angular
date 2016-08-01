

import logging
import sys
import inject
sys.path.insert(0,'../../python')


logging.getLogger().setLevel(logging.INFO)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine
from model.registry import Registry




class WampMain(ApplicationSession):

    def __init__(self,config=None):
        logging.debug('instanciando WampMain')
        ApplicationSession.__init__(self, config)


    @coroutine
    def onJoin(self, details):
        logging.debug('inicio consulta de los listados')
        
        id = sys.argv[1]

        data = yield from self.call('sileg.getPlaceById', [id])
        logging.info(data[0].__dict__)



if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        reg = inject.instance(Registry)
        registry = reg.getRegistry('wamp')
        url = registry.get('url')
        realm = registry.get('realm')
        debug = registry.get('debug')
        
        
        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,  serializers=[json])
        runner.run(WampMain)
