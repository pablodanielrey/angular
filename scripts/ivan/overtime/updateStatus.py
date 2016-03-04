import logging
import sys
import inject
import datetime
sys.path.insert(0,'../../../python')

from model.config import Config
logging.getLogger().setLevel(logging.DEBUG)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine

'''
python3 updateStatus.py userId requestId status
python3 updateStatus.py 1 1b4a8f46-9d9f-48a8-8ddb-078d361f8e05 APPROVED
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
        logging.info("********** MODIFICAR ESTADO DE REQUERIMIENTO DE HORA EXTRA **********")

        if len(sys.argv) < 4:
            sys.exit("Error de parámetros")


        userId = sys.argv[1]
        requestId = sys.argv[2]
        status = sys.argv[3]

        overtimeId = yield from self.call('overtime.updateStatus', userId, requestId, status)


if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
