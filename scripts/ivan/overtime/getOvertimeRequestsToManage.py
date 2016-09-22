import logging
import sys
import inject
sys.path.insert(0,'../../../python')

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
        logging.info("********** REQUERIMIENTOS DE HORAS EXTRAS PARA ADMINISTRAR **********")

        if len(sys.argv) < 3:
            sys.exit("Error de parámetros")

        if sys.argv[2] != 'ROOT' and sys.argv[2] != 'TREE':
            sys.exit("Error de parámetros")
                    
        userId = sys.argv[1]
        group = sys.argv[2]

        logging.info("********** USUARIO: " + userId + " **********")
        logging.info("********** GRUPO: " + group + " **********")


        states = []
        if len(sys.argv) > 3:
            for i in range(3 , len(sys.argv)):
                if sys.argv[i] != 'APPROVED' and sys.argv[i] != 'PENDING' and sys.argv[i] != 'REJECTED':
                    sys.exit("Error de parámetros")
                states.append(sys.argv[i])

        requests = yield from self.call('overtime.getOvertimeRequestsToManage', userId, group, states)

        for request in requests:
            print(request)

if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
