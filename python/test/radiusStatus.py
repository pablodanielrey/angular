
import json
import datetime
import pytz
from dateutil.tz import tzlocal
import dateutil
from dateutil.parser import parse
import sys
sys.path.append('../../python')

import inject
inject.configure()

import logging

#from model.registry import Registry
#from model.connection.connection import Connection
#from model.offices.offices import Office
#from model.users.users import User, UserPassword


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    import sys
    root = sys.argv[1]

    import re
    rdate = re.compile('(\w*\s+\w*\s+\d*\s+\d\d:\d\d:\d\d\s+\d\d\d\d)')
    rip = re.compile('NAS-IP-Address = (\d+\.\d+\.\d+\.\d+)')
    rmac = re.compile('NAS-Identifier = "(.*)"')
    rcds = re.compile('Called-Station-Id = "(.*)"')
    rcis = re.compile('Calling-Station-Id = "(.*)"')
    ru = re.compile('User-Name = "(.*)"')

    reg = re.compile('(?P<record>^\w+.*$\n(.*\n)*?)^\n', re.M)

    records = []
    import os
    for r,d,files in os.walk(root):
        for f in files:
            with open('{}/{}'.format(r,f), 'r') as log:
                record = {}
                cont = log.read()

                for m in reg.finditer(cont):
                    rec = m.group(1)

                    m = rdate.search(rec)
                    if m:
                        record['date'] = parse(m.group(1))

                    m = rip.search(rec)
                    if m:
                        record['ip ap'] = m.group(1)

                    m = rmac.search(rec)
                    if m:
                        record['mac'] = m.group(1)

                    m = rcds.search(rec)
                    if m:
                        record['destino'] = m.group(1)

                    m = rcis.search(rec)
                    if m:
                        record['origen'] = m.group(1)

                    m = ru.search(rec)
                    if m:
                        record['usuario'] = m.group(1)

                    records.append(record)

    for r in records:
        logging.info(r)
