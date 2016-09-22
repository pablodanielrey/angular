# -*- coding: utf-8 -*-

import pprint
import logging
import csv
import sys
from zksoftware.zkSoftware import ZkSoftware

logging.getLogger().setLevel(logging.INFO)

zk = ZkSoftware("192.168.19.19", 80)

logs = zk.getAttLog('ALL')
w = csv.writer(sys.stdout, delimiter=';')
for l in logs:
    w.writerow(l.values())
