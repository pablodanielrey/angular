import logging
import sys
import inject
sys.path.insert(0,'../../../python')

from model.config import Config
logging.getLogger().setLevel(logging.DEBUG)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine


'''
python3 getOvertimeRequestsByState userId #retorna los requerimientos de todos los usuarios
python3 getOvertimeRequestsByState userId state1 state2 state3 ... #retorna los requerimientos de los usuarios con el id pasado como parametro
python3 getOvertimeRequestsByState e43e5ded-e271-4422-8e85-9f1bc0a61235 #retorna los requerimientos de los usuarios con el id pasado como parametro

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
        logging.info("********** REQUERIMIENTOS DE HORAS EXTRAS DE LOS USUARIOS **********")

        if len(sys.argv) < 2:
            sys.exit("Error de parámetros")

        user = sys.argv[1]

        logging.info("********** USUARIO: " + user + " **********")

        users = [user]

        states = []
        if len(sys.argv) > 2:
            for i in range(2 , len(sys.argv)):
                if sys.argv[i] != 'APPROVED' and sys.argv[i] != 'PENDING' and sys.argv[i] != 'REJECTED':
                    sys.exit("Error de parámetros")
                states.append(sys.argv[i])

        requests = yield from self.call('overtime.getOvertimeRequests', users, states)

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
