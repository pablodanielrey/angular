# -*- coding: utf-8 -*-
'''
    Se conecta al router wamp y hace correr el Wamp
'''
if __name__ == '__main__':

    import sys
    import logging
    import inject
    sys.path.insert(0, '../python')

    logging.basicConfig(level=logging.DEBUG)

    from autobahn.asyncio.wamp import ApplicationRunner
    from model.registry import Registry
    from actions.login.login import LoginWamp

    inject.configure()

    reg = inject.instance(Registry)
    registry = reg.getRegistry('dcsys')
    url = registry.get('url')
    realm = registry.get('realm')
    debug = registry.get('debug')

    runner = ApplicationRunner(url=url, realm=realm, debug=debug, debug_wamp=debug, debug_app=debug)
    runner.run(LoginWamp)
