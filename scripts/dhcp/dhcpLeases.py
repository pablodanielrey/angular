import json
import datetime
import pytz
import sys
sys.path.append('../../python')

import inject
inject.configure()

import uuid
import logging
import uuid

from model.registry import Registry
from model.connection.connection import Connection


def isExist(con, mac):
    cur = con.cursor()
    try:
        cur.execute('select mac from dhcp.hosts where mac = %s',(mac,))
        return cur.rowcount > 0
    finally:
        cur.close()

def addHost(con, ip, mac):
    cur = con.cursor()
    try:
        rid = str(uuid.uuid4())
        cur.execute('insert into dhcp.hosts (id, ip, mac) values (%s, %s, %s)', (rid, ip, mac))
    finally:
        cur.close()

archivo = sys.argv[1]

f = open(archivo, 'r')

conjunto = set()


try:
    #print(f.readline())
    for line in f:
        if 'hardware ethernet' in line:
            mac = (line[20:-2])
            conjunto.add(mac)
    print(conjunto)
    print(len(conjunto))
finally:
    f.close()


reg = inject.instance(Registry)
conn = Connection(reg.getRegistry('dcsys'))
con = conn.get()
try:

    for mac in conjunto:
        if isExist(con, mac):
            print('ya existe {}'.format(mac))
        else:
            print('no existe {}'.format(mac))
            ip = '166.166.166.166'
            addHost(con, ip, mac)

        con.commit()

finally:
    conn.put(con)
