# -*- coding: utf-8 -*-
'''
    Se conecta al router wamp y hace correr el Wamp
'''
import inject
inject.configure()



if __name__ == '__main__':

    import sys
    import logging
    sys.path.insert(0, '../python')

    logging.basicConfig(level=logging.DEBUG)

    #import txaio
    #txaio.use_asyncio()
    #txaio.start_logging(level='debug')

    from autobahn.asyncio.wamp import ApplicationRunner
    from model.registry import Registry
    from actions.login.login import LoginWamp

    reg = inject.instance(Registry)
    registry = reg.getRegistry('wamp')
    url = registry.get('url')
    realm = registry.get('realm')
    debug = registry.get('debug')

    runner = ApplicationRunner(url=url, realm=realm)
    runner.run(LoginWamp)
