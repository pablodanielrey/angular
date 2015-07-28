# -*- coding: utf-8 -*-


'''
    Ejecuta el protocolo Wamp del modelo del firmware
'''
if __name__ == '__main__':

    import sys, logging, inject
    sys.path.insert(0,'../../python')

    logging.basicConfig(level=logging.DEBUG)

    from autobahn.asyncio.wamp import ApplicationRunner
    from network.wampFirmware import WampFirmware
    from model.config import Config

    def config_injector(binder):
        binder.bind(Config,Config('firmware-config.cfg'))

    inject.configure(config_injector)
    config = inject.instance(Config)

    url = config.configs['firmware_url']
    realm = config.configs['firmware_realm']
    debug = config.configs['firmware_debug']

    runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug)
    runner.run(WampFirmware)
