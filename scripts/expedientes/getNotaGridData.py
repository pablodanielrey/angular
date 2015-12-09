import sys, inject
sys.path.insert(0,'../../python')

from model.config import Config

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine

'''
python3 getNotaGridData.py search
python3 getNotaGridData.py "valor a buscar"
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
        print("********** NOTA GRID DATA **********")
        
        id = sys.argv[1]
        
        rows = yield from self.call('expedientes.getNotaGridData')
        print(rows)

if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
