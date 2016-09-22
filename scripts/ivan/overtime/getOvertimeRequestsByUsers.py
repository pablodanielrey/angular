import logging
import sys
import inject
sys.path.insert(0,'../../../python')

from model.config import Config
logging.getLogger().setLevel(logging.DEBUG)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine

'''
python3 getOvertimeRequestsByUser.py state #retorna los requerimientos de todos los usuarios
python3 getOvertimeRequestsByUser.py state userId1 userId2 userId3 ... #retorna los requerimientos de los usuarios con el id pasado como parametro
python3 getOvertimeRequestsByUser.py APPROVED
python3 getOvertimeRequestsByUser.py APPROVED "4b89c515-2eba-4316-97b9-a6204d344d3a  3e7b36fb-1530-4ef5-9088-4e5990f26a90"
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

        state = sys.argv[1]

        if state != 'APPROVED' and state != 'PENDING' and state != 'REJECTED':
            sys.exit("Error de parámetros")

        logging.info("********** ESTADO: " + state + " **********")

        states = [state]

        users = []
        if len(sys.argv) > 2:
            for i in range(2 , len(sys.argv)):
                users.append(sys.argv[i])

        requests = yield from self.call('overtime.getOvertimeRequests', users, states)

        for request in requests:
            print(request)
            
        sys.exit()

if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
