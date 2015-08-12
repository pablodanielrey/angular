# -*- coding: utf-8 -*-
import sys
sys.path.append('../../python')

import logging
import inject
import base64

from model.config import Config


def config_injector(binder):
    binder.bind(Config, Config('server-config.cfg'))

inject.configure(config_injector)
logging.getLogger().setLevel(logging.DEBUG)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine


class WampMain(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando wampClient')
        ApplicationSession.__init__(self, config)

    @coroutine
    def onJoin(self, details):
        logging.debug('session joined')

        ''' aca se ejecutan las llamadas wamp '''
        try:
            ids = yield from self.call('system.files.findAllIds')
            for id in ids:
                logging.info('buscando archivo {}'.format(id))
                f = yield from self.call('system.files.find', id)
                logging.info('archivo : {}'.format(f))

                ''' el contenido del archivo esta en base64 '''
                content = base64.b64decode(f['content'])
                with open('/tmp/ff/{}-{}'.format(f['id'], f['name']), 'wb') as ff:
                    ff.write(content)

        except Exception as e:
            logging.exception(e)

if __name__ == '__main__':

    from autobahn.asyncio.wamp import ApplicationRunner

    config = inject.instance(Config)
    runner = ApplicationRunner(url=config.configs['server_url'], realm=config.configs['server_realm'], debug=True, debug_wamp=True, debug_app=True)
    runner.run(WampMain)
