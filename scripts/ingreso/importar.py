import logging
import sys
import re
import inject
sys.path.insert(0, '../../python')

from model.config import Config
logging.getLogger().setLevel(logging.INFO)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine


def config_injector(binder):
    binder.bind(Config, Config('server-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)


class WampMain(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando WampMain')
        ApplicationSession.__init__(self, config)

    @coroutine
    def onJoin(self, details):
        logging.debug('importando alumnos')

        users = [line.strip() for line in open(sys.argv[1])]
        for u in users:
            u = u.replace("\"", '')
            columns = u.split(',')

            m = re.search('(?P<type>.*\s+)(?P<dni>[a-zA-Z]*\d+)', columns[3])
            dni = m.group('dni')
            if dni is None:
                logging.warn('{} no tiene DNI'.format(u))
                continue

            name = columns[2]
            lastname = columns[1]
            logging.info('dni : {} - name : {} - lastname: {}'.format(dni, name.title(), lastname.title()))

            user = {
                'dni': dni,
                'name': name,
                'lastname': lastname
            }
            data = yield from self.call('users.persistUser', user)
            logging.info('usuario creado : {}'.format(data))

        sys.exit(0)


if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer

        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url, realm=realm, debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
