# -*- coding: utf-8 -*-
'''
    Se conecta al router wamp y hace correr el Wamp de insercion laboral
'''
if __name__ == '__main__':

    import sys
    import logging
    import inject
    sys.path.insert(0, '../python')

    logging.basicConfig(level=logging.DEBUG)

    from autobahn.asyncio.wamp import ApplicationRunner
    from model.config import Config
    from actions.systems.laboralinsertion.laboralInsertion import LaboralInsertionWamp

    def config_injector(binder):
        binder.bind(Config, Config('server-config.cfg'))

    inject.configure(config_injector)
    config = inject.instance(Config)

    url = config.configs['server_url']
    realm = config.configs['server_realm']
    debug = config.configs['server_debug']

    runner = ApplicationRunner(url=url, realm=realm, debug=debug, debug_wamp=debug, debug_app=debug)
    runner.run(LaboralInsertionWamp)
