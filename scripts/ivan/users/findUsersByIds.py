import logging
import sys
import inject
sys.path.insert(0,'../../../python')

from model.config import Config
logging.getLogger().setLevel(logging.INFO)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine

'''
python3 findUsersByIds d44e92c1-d277-4a45-81dc-a72a76f6ef8d
python3 findUsersByIds id1 id2 id3 ...
'''


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
        logging.info("********** USUARIOS **********")

        if len(sys.argv) < 2:
            sys.exit("Error de parámetros")

        ids = []
        for i in range(1 , len(sys.argv)):
            ids.append(sys.argv[i])

        users = yield from self.call('users.findUsersByIds', ids)
        for user in users:
            logging.info(user)


if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
