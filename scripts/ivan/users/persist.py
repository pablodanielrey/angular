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
python3 persist.py dni name lastname city country address genre birthdate residence_city
python3 persist.py 31111120 "Pepe Pipo" "Pompin Pampon" "La Plata" "Argentina" "31 Nro 94" "Masculino" "10/09/1984" "La Plata"
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
        logging.info("********** PERSISTIR USUARIO **********")
        birthdate = datetime.strptime("2000-10-10 00:00", "%Y-%m-%d %H:%M")
        logging.info(birthdate.strftime("%Y-%m-%d"))
        '''
        if len(sys.argv) < 10:
            sys.exit("Error de parámetros")

        print("cssssssssssssssss")
        print(sys.argv[8])


        print("bbbbbbbbbbbbb")
        user = {
            'dni':sys.argv[1],
            'name':sys.argv[2],
            'lastname':sys.argv[3],
            'city':sys.argv[4],
            'country':sys.argv[5],
            'address':sys.argv[6],
            'genre':sys.argv[7],
            'birthdate':birthdate,
            'residence_city':sys.argv[9],
            'version':0
        }

        print("AAAAAAAAAAAA")
        userId = yield from self.call('users.persistUser', user)
        logging.info(userId)
        '''

if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
