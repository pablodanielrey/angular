import sys, logging
from firmware import Firmware
from itertools import zip_longest
import camabio

logging.getLogger().setLevel(logging.INFO)
port = sys.argv[1]

f = Firmware(port)
f.start()
try:
    (huella,template) = f.enroll()

    logging.info(huella)
    logging.info(template)

finally:
    f.stop()
