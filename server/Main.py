# -*- coding: utf-8 -*-
import signal, sys, json, traceback, inject, time, logging

#sys.path.append('../python')
sys.path.insert(0,'../python')


from model.config import Config
from model.session import Session

from model.utils import Periodic
from model.systems.assistance.assistance import Assistance
from model.systems.assistance.fails import Fails
from model.systems.assistance.date import Date

import network.websocket
import model.systems.assistance.network


def config_injector(binder):
    binder.bind(Config,Config('server-config.cfg'))
    binder.bind(Session,Session())


"""
    chequeo de horarios de asistencia.
    despues hay que ver donde queda mejor
"""
def _checkAssistanceSchedule(assistance,f):
    logging.info('chequeando schedules')
    date = inject.instance(Date)
    (users,fails) = assistance.checkSchedule(date.parse('2015-03-31 00:00:00'), date.parse('2015-04-01 00:00:00'))
    f.toCsv('/tmp/f.csv',users,fails)
    for user in users:
        ffails = f.filterUser(user['id'],fails)
        f.toCsv('/tmp/{}-{}-{}.csv'.format(user['dni'],user['name'],user['lastname']),users,ffails)



if __name__ == '__main__':

  logging.basicConfig(level=logging.DEBUG)

  inject.configure(config_injector)
  config = inject.instance(Config)

  fails = inject.instance(Fails)
  assistance = inject.instance(Assistance)
  #rt = utils.Periodic(15 * 60, _checkAssistanceSchedule,assistance)
  #_checkAssistanceSchedule(assistance,fails)
  #sys.exit(0)

  (reactor,port,factory) = network.websocket.getPort()

  def close_sig_handler(signal,frame):
      #rt.stop()
      port.stopListening()
      reactor.stop()
      sys.exit()

  signal.signal(signal.SIGINT,close_sig_handler)

  logging.debug('Ejecutando servidor de acciones')
  reactor.run()
