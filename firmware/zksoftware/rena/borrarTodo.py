# -*- coding: utf-8 -*-

import pprint
import logging
from zksoftware.zkSoftware import ZkSoftware

logging.getLogger().setLevel(logging.DEBUG)

zk = ZkSoftware("192.168.19.19", 80)
zk._clearData(3)
zk._clearData(1)
