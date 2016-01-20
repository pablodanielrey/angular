# -*- coding: utf-8 -*-
import signal
import sys
import inject
import logging

# sys.path.append('../python')
sys.path.insert(0, '../python')

from model.config import Config
from model.session import Session

import network.websocket


def config_injector(binder):
    binder.bind(Config, Config('server-config.cfg'))
    binder.bind(Session, Session())


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    inject.configure(config_injector)
    config = inject.instance(Config)

    (loop, server, factory) = network.websocket.getLoop()
    # (reactor,port,factory) = network.websocket.getPort()

    def close_sig_handler(signal, frame):
        server.close()
        loop.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    logging.debug('Ejecutando servidor de acciones')
    try:
        loop.run_forever()
    except Exception as e:
        logging.exception(e)
