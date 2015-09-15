import logging
import sys
import inject
from datetime import datetime
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
        logging.info("********** CARGAR REQUERIMIENTO DE HORA EXTRA **********")

        if len(sys.argv) < 8:
            sys.exit("Error de parámetros")

        
        requestorId = sys.argv[1]
        userId = sys.argv[2]
        beginDate = sys.argv[3]
        beginTime = sys.argv[4]
        endDate = sys.argv[5]
        endTime = sys.argv[6]
        reason =  sys.argv[7]

        begin = datetime.strptime(beginDate + " " + beginTime, "%Y-%m-%d %H:%M")
        end = datetime.strptime(endDate + " " + endTime, "%Y-%m-%d %H:%M")

     
        logging.info("********** SOLICITADO POR: " + requestorId + " **********")
        logging.info("********** USUARIO: " + userId + " **********")
        logging.info("********** INICIO: " + begin.strftime('%Y-%m-%d %H:%M') + " **********")
        logging.info("********** FIN: " + end.strftime('%Y-%m-%d %H:%M') + " **********")

        overtimeId = yield from self.call('overtime.requestOvertime', requestorId, userId, begin, end, reason)

        logging.info("********** ID DEL REQUERIMIENTO SOLICITADO: " + overtimeId + " **********")

if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
