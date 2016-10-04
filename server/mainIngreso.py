# -*- coding: utf-8 -*-
'''
    Se conecta al router wamp y hace correr el Wamp de Users
'''
if __name__ == '__main__':

    import sys
    import logging
    import inject
    sys.path.insert(0, '../python')

    logging.basicConfig(level=logging.DEBUG)

    from autobahn.asyncio.wamp import ApplicationRunner
    from model.registry import Registry
    from actions.systems.ingreso.users import IngresoWamp

    from model.registry import Registry

    reg = inject.instance(Registry)
    registry = reg.getRegistry('wamp')
    url = registry.get('url')
    realm = registry.get('realm')
    debug = registry.get('debug')

    runner = ApplicationRunner(url=url, realm=realm)
    runner.run(IngresoWamp)
