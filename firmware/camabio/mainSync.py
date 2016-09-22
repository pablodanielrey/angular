# -*- coding: utf-8 -*-
import sys, logging, inject
sys.path.insert(0,'../../python')

logging.basicConfig(level=logging.DEBUG)

from model.config import Config

def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)


'''
    Ejecuta el protocolo Wamp del sincronizador
'''
if __name__ == '__main__':

    from autobahn.asyncio.wamp import ApplicationRunner
    from autobahn.wamp.serializer import JsonSerializer
    from sync import WampSync


    url = config.configs['server_url']
    realm = config.configs['server_realm']
    debug = config.configs['server_debug']

    json = JsonSerializer()
    runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers = [json])
    runner.run(WampSync)
