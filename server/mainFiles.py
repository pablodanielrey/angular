# -*- coding: utf-8 -*-
'''
    Se conecta al router wamp y hace correr el Wamp de Files
'''
if __name__ == '__main__':

    import sys
    import logging
    import inject
    sys.path.insert(0, '../python')

    logging.basicConfig(level=logging.DEBUG)

    from autobahn.asyncio.wamp import ApplicationRunner
    from actions.systems.files.files import FilesWamp
    from model.registry import Registry

    inject.configure()

    reg = inject.instance(Registry)
    registry = reg.getRegistry('wamp')
    url = registry.get('url')
    realm = registry.get('realm')
    debug = registry.get('debug')

    runner = ApplicationRunner(url=url, realm=realm)
    runner.run(FilesWamp)
