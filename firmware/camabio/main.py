import sys, logging, time
from firmware import FirmwareReader
from itertools import zip_longest
import threading
import camabio
import signal


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
                logging.info('cerrando enrolador')
                return

            if line == 'e\n':
                logging.info('c')
                self.firmware.cancel()
                logging.info('e')
                (h,t) = self.firmware.enroll()
                logging.info('ee')
                if h:
                    logging.info('huella {} - {}'.format(h,t))


lend = threading.Lock()
lend.acquire()

def signal_handler(signal,frame):
    global end, lend
    logging.info('ctrl+c')
    end = True
    lend.release()

signal.signal(signal.SIGINT,signal_handler)

logging.getLogger().setLevel(logging.INFO)
port = sys.argv[1]
f = FirmwareReader(port)
f.start()
try:
    i = Identifier(f)
    e = Enroller(f)

    i.start()
    e.start()

    lend.acquire()

    f.cancel()
    e.join()
    i.join()

finally:
    f.stop()
