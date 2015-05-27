import sys, logging, time
from firmware import FirmwareReader, Firmware
from itertools import zip_longest
import threading
import camabio
import signal
import inject

sys.path.append('../../python')
from network import websocket

from model.config import Config

end = False

class Identifier(threading.Thread):

    def __init__(self, firmware):
        threading.Thread.__init__(self)
        self.firmware = firmware

    def run(self):
        global end
        while True:

            if end:
                return

            h = self.firmware.identify()
            if h:
                logging.info('Se ha identificado la huella {}'.format(h))



class Enroller(threading.Thread):
    def __init__(self, firmware):
        threading.Thread.__init__(self)
        self.firmware = firmware

    def run(self):
        global end
        while True:
            if end:
                return

            logging.info('Ingrese exit/e')
            line = sys.stdin.readline()
            logging.info('linea leida {}'.format(line))

            if line == 'exit\n':
                logging.info('cerrando programa')
                end = True
                return

            if line == 'e\n':
                logging.info('e')
                (h,t) = self.firmware.enroll()
                logging.info('ee')
                if h:
                    logging.info('huella {} - {}'.format(h,t))






def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))

inject.configure(config_injector)

def signal_handler(signal,frame):
    global end
    logging.info('ctrl+c')
    end = True

signal.signal(signal.SIGINT,signal_handler)

logging.getLogger().setLevel(logging.DEBUG)
port = sys.argv[1]
"""
f = FirmwareReader(port)
f.start()
try:
    i = Identifier(f)
    e = Enroller(f)

    i.start()
    e.start()

    e.join()
    i.join()

finally:
    f.stop()
"""



#f = Firmware(port)
#f.start()
try:
    (reactor,port,factory) = websocket.getPort()

    def close_sig_handler(signal,frame):
      port.stopListening()
      reactor.stop()
      sys.exit()

    signal.signal(signal.SIGINT,close_sig_handler)

    logging.debug('Ejecutando servidor de acciones')
    reactor.run()

finally:
    #f.stop()
    pass
