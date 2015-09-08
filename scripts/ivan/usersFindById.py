import logging
import sys
import inject
sys.path.insert(0,'../../python')

from model.config import Config
logging.getLogger().setLevel(logging.DEBUG)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine



def config_injector(binder):
    binder.bind(Config,Config('server-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)


class WampMain(ApplicationSession):

    def __init__(self,config=None):
        logging.debug('instanciando WampMain')
        ApplicationSession.__init__(self, config)


    @coroutine
    def onJoin(self, details):
        user1 = yield from self.call('users.findById', '565d7d2e-3b82-41d6-8617-a77a7e723d50') #italo boggia
        user2 = yield from self.call('users.findById', '99a18a05-73e0-4e31-babe-5ddd8d381ee7') #vanesa ramirez

        logging.info("********** USUARIOS CONSULTADOS **********")
        logging.info(user1)
        logging.info(user2)



if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
