import logging
import sys
import inject
sys.path.insert(0,'../../python')

from model.config import Config
#logging.getLogger().setLevel(logging.INFO)

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
        #logging.debug('instanciando WampMain')
        ApplicationSession.__init__(self, config)


    @coroutine
    def onJoin(self, details):

        if len(sys.argv) < 3:
            sys.exit("Error de parámetros")

        dni = sys.argv[1]
        email = sys.argv[2]

        user = yield from self.call('users.findByDni', dni)
        print(user["id"])
        
        userEmail = {
          'user_id': user["id"],
          'email': email,
          'confirmed': False
        }
        
        emailId = yield from self.call('users.mails.persistMail', userEmail)

        yield from self.call('users.mails.sendEmailConfirmation', emailId)

        print("***** Email alternativo agregado: " + user["name"] + " " + user["lastname"] + " " + email + " (" + emailId + ")")
        
        sys.exit()


if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
