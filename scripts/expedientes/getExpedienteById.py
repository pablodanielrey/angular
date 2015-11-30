import sys, inject
sys.path.insert(0,'../../python')

from model.config import Config

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine

'''
python3 getExpedienteById.py id
python3 getExpedienteById.py e43e5ded-e271-4422-8e85-9f1bc0a61235
'''

def config_injector(binder):
    binder.bind(Config,Config('server-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)

class WampMain(ApplicationSession):

    def __init__(self,config=None):
        ApplicationSession.__init__(self, config)

    @coroutine
    def onJoin(self, details):
        print("********** EXPEDIENTE BY ID **********")
        
        id = sys.argv[1]
        
        row = yield from self.call('expedientes.getExpedienteById', id)
        print(row)

if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
