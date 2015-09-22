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
python3 getWorkedOvertime.py userId date #horas trabajadas correspondientes a overtime
python3 getWorkedOvertime.py e43e5ded-e271-4422-8e85-9f1bc0a61235 "10/10/2015 00:00"

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
        logging.info("********** MINUTOS TRABAJADOS DE REQUERIMIENTOS DE HORAS EXTRAS APROBADAS **********")

        if len(sys.argv) < 3:
            sys.exit("Error de parámetros")


        userId = sys.argv[1]
        dateParam = sys.argv[2]
        
        date = datetime.datetime.strptime(dateParam, "%d/%m/%Y %H:%M")

        yield from self.call('overtime.getWorkedOvertime', userId, date)
        
        #logging.info(minutes)

      
if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
