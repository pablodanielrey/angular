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
python3 persist.py userId email [confirmed = False]
python3 persist.py d44e92c1-d277-4a45-81dc-a72a76f6ef8d example@gmail.com
python3 persist.py d44e92c1-d277-4a45-81dc-a72a76f6ef8d example2@gmail.com True
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
        logging.info("********** PERSISTIR EMAIL **********")

        if len(sys.argv) < 3:
            sys.exit("Error de parámetros")


        email = {
            'user_id':sys.argv[1],
            'email':sys.argv[2],
            'confirmed':False,
        }

        if len(sys.argv) == 3:
            email['confirmed'] = True

        emailId = yield from self.call('users.mails.persistMail', email)
        logging.info(emailId)

if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
