# -*- coding: utf-8 -*-
'''
    Se conecta al router wamp y hace correr el Wamp de Users
'''

import inject
inject.configure()

if __name__ == '__main__':

    import sys
    import logging
    sys.path.insert(0, '../python')

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)

    from autobahn.asyncio.wamp import ApplicationRunner
    from actions.systems.tutors.tutors import TutorsWamp
    from model.registry import Registry

    reg = inject.instance(Registry)
    registry = reg.getRegistry('wamp')
    url = registry.get('url')
    realm = registry.get('realm')
    debug = registry.get('debug')

    runner = ApplicationRunner(url=url, realm=realm)
    runner.run(TutorsWamp)
