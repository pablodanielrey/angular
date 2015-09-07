import logging
import sys
import inject
import datetime
sys.path.insert(0,'../../python')

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
        email = {
            'id':'70574fb8-f31e-4e01-a3d5-c128bec4ba20',
            'email':'ivancas84@gmail.com',
            'user_id':'d44e92c1-d277-4a45-81dc-a72a76f6ef8d',
            'confirmed':False
        }
        yield from self.call('users.mails.sendEmailConfirmation', email)

        logging.info("********** CONFIRMACION POR EMAIL ENVIADA **********")

if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
