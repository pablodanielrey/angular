# -*- coding: utf-8 -*-
import signal, sys, json, traceback, inject, time, logging

from model.config import Config
from model.session import Session

from model.utils import Periodic
from model.systems.assistance.assistance import Assistance

import network.websocket



def config_injector(binder):
    binder.bind(Session,Session())


"""
    chequeo de horarios de asistencia.
    despues hay que ver donde queda mejor
"""
def _checkAssistanceSchedule(assistance):
    assistance.checkSchedule()


if __name__ == '__main__':

  logging.basicConfig(level=logging.DEBUG);

  inject.configure(config_injector)
  config = inject.instance(Config)


  assistance = inject.instance(Assistance)
  #rt = utils.Periodic(15 * 60, _checkAssistanceSchedule,assistance)
  _checkAssistanceSchedule(assistance)

  """
  reactor = network.websocket.getReactor()

  def close_sig_handler(signal,frame):
      rt.stop()
      reactor.stopListening()
      sys.exit()

  signal.signal(signal.SIGINT,close_sig_handler)

  logging.debug('Ejecutando servidor de acciones')
  reactor.run()

  logging.debug('iniciando bucle infinito')

  while True:
      time.sleep(1000)
  """
