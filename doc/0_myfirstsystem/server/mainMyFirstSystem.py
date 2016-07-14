# -*- coding: utf-8 -*-
'''
    Se conecta al router wamp y hace correr el Wamp de MyFirstSystem
'''
if __name__ == '__main__':

    import sys
    import logging
    import inject
    inject.configure()

    logging.basicConfig(level=logging.DEBUG)

    from autobahn.asyncio.wamp import ApplicationRunner
    from wamp import MyFirstSystemWamp
    from model.registry.registry import Registry

    reg = inject.instance(Registry)
    registry = reg.getRegistry('wamp')
    url = registry.get('url')
    realm = registry.get('realm')
    debug = registry.get('debug')

    runner = ApplicationRunner(url=url, realm=realm)
    runner.run(MyFirstSystemWamp)
