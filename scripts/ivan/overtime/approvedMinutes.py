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
python3 approvedMinutes.py userId begin [end] #horas aprobadas del usuario en un determinado periodo
python3 approvedMinutes.py e43e5ded-e271-4422-8e85-9f1bc0a61235 "10/10/2015 00:00"
python3 approvedMinutes.py e43e5ded-e271-4422-8e85-9f1bc0a61235 "10/10/2015 00:00" "20/10/2015 00:00"

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
        logging.info("********** MINUTOS APROBADOS DE REQUERIMIENTOS DE HORAS EXTRAS APROBADAS **********")

        if len(sys.argv) < 3:
            sys.exit("Error de parámetros")


        userId = sys.argv[1]
        beginParam = sys.argv[2]
        endParam = sys.argv[3]
        
        begin = datetime.datetime.strptime(beginParam, "%d/%m/%Y %H:%M").date()
        end = datetime.datetime.strptime(endParam, "%d/%m/%Y %H:%M").date()
        
        print(end)
        
        minutes = yield from self.call('overtime.getMinutesApproved', userId, begin, end)
        
        logging.info(minutes)

      
if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
