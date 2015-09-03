import logging
import sys
import inject
sys.path.insert(0,'../../python')

from model.config import Config
logging.getLogger().setLevel(logging.INFO)

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
        user = {
            'dni':'31000123',
            'name':'Pepe',
            'lastname':'Pompin',
            'city':'La Plata',
            'country':'Argentina',
            'adress':'33 Nº 3333',
            'genre':'Masculino',
            'birthdate':datetime.datetime(1980, 7, 20),
            'residence_city':'La Plata',
            'version':0
        }

        userId = yield from self.call('users.persistUser', user)

        logging.info("********** ID DEL USUARIO AGREGADO **********")
        logging.info(userId)

if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
