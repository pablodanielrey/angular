# -*- coding: utf-8 -*-
import signal, sys, json, traceback, inject, time, logging

from model.config import Config
from model.session import Session

import network.websocket



def config_injector(binder):
    binder.bind(Session,Session())


if __name__ == '__main__':

  logging.basicConfig(level=logging.DEBUG);

  inject.configure(config_injector)
  config = inject.instance(Config)


  reactor = network.websocket.getReactor()

  def close_sig_handler(signal,frame):
      sys.exit()

  signal.signal(signal.SIGINT,close_sig_handler)

  logging.debug('Ejecutando servidor de acciones')
  reactor.run()

  logging.debug('iniciando bucle infinito')
  while True:
    time.sleep(1000)
