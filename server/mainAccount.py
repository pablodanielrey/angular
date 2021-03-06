# -*- coding: utf-8 -*-
'''
    Se conecta al router wamp y hace correr AssistanceWamp y JustificationsWamp
'''
if __name__ == '__main__':

    import sys
    import logging
    import inject
    inject.configure()

    sys.path.insert(0, '../python')

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)

    from autobahn.asyncio.wamp import ApplicationRunner
    from actions.systems.account.account import AccountWamp
    from model.registry import Registry

    reg = inject.instance(Registry)
    registry = reg.getRegistry('wamp')
    url = registry.get('url')
    realm = registry.get('realm')
    debug = registry.get('debug')

    logging.info('iniciando app en {} {} {}'.format(url, realm, debug))
    runner = ApplicationRunner(url=url, realm=realm)
    runner.run(AccountWamp)
