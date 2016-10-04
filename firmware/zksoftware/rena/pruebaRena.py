# -*- coding: utf-8 -*-

import pprint
import logging
from zksoftware.zkSoftware import ZkSoftware

logging.getLogger().setLevel(logging.INFO)

zk = ZkSoftware("192.168.19.19", 80)

pp = pprint.PrettyPrinter(indent=4)

#logging.info(zk.getUserInfo("27294557"))
logging.info(pp.pprint(zk.getAttLog("27294557")))
zk.clearAttLogs()
