# -*- coding: utf-8 -*-
import sys, logging, inject
sys.path.insert(0,'../../python')

from model.config import Config

logging.basicConfig(level=logging.DEBUG)

def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)


'''
    Ejecuta el protocolo Wamp del modelo del firmware
'''
if __name__ == '__main__':

    from autobahn.asyncio.wamp import ApplicationRunner
    from autobahn.wamp.serializer import JsonSerializer
    from network.wampFirmware import WampFirmware




    url = config.configs['firmware_url']
    realm = config.configs['firmware_realm']
    debug = config.configs['firmware_debug']

    json = JsonSerializer()
    runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
    runner.run(WampFirmware)
