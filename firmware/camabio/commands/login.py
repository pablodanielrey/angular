# -*- coding: utf-8 -*-
import sys, logging

from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    if len(sys.argv) < 3:
        logging.warn('python3 {} {} {}'.format(sys.argv[0],'dni','password'))
        sys.exit(1)

    dni = sys.argv[1]
    password = sys.argv[2]


    class WampCommand(ApplicationSession):

        def __init__(self,config=None):
            logging.debug('instanciando WampMain')
            ApplicationSession.__init__(self, config)


        def _userIdentified(self,data):
            logging.info('--- Usuario identificado ---')
            logging.info(data)
            sys.exit(0)

        @coroutine
        def onJoin(self, details):
            logging.debug('session joined')

            yield from self.subscribe(self._userIdentified,'assistance.firmware.identify')

            try:
                yield from self.call('assistance.firmware.login',dni,password)

            except Exception as e:
                logging.exception(e)
                sys.exit(1)



    from autobahn.asyncio.wamp import ApplicationRunner

    runner = ApplicationRunner(url='ws://localhost:8000/ws',realm='assistance',debug=True, debug_wamp=True, debug_app=True)
    runner.run(WampCommand)
