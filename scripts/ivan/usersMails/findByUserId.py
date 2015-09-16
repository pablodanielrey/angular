import logging
import sys
import inject
sys.path.insert(0,'../../../python')

from model.config import Config
logging.getLogger().setLevel(logging.INFO)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine

'''
python3 findByUserId.py userId
python3 findByUserId.py d44e92c1-d277-4a45-81dc-a72a76f6ef8d
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
        logging.info("********** EMAILS DEL USUARIO **********")

        if len(sys.argv) < 2:
            sys.exit("Error de parámetros")

        id = sys.argv[1]

        mails = yield from self.call('users.mails.findMails', id)
        for mail in mails:
            logging.info(mail)


if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
