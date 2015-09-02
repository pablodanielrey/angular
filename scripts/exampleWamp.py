import logging
import sys

logging.getLogger().setLevel(logging.INFO)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine


sys.argv[1]




class WampMain(ApplicationSession):

    def __init__(self,config=None):
        logging.debug('instanciando WampMain')
        ApplicationSession.__init__(self, config)


    @coroutine
    def onJoin(self, details):
        logging.debug('inicio consulta de los listados')

        yield from self.call('assistance.justifications.getJustifications', sys.argv[1], sys.argv[2])


        while True:
            try:
                logging.info('identificando')
                yield from self.call('assistance.firmware.identify')

            except Exception as e:
                logging.exception(e)





if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['firmware_url']
        realm = config.configs['firmware_realm']
        debug = config.configs['firmware_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampFirmware)
