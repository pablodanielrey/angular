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

import re

from model.registry import Registry
from model.connection.connection import Connection

#funcion que controla si exixte la mac en la base
def isExist(con, mac):
    cur = con.cursor()
    try:
        cur.execute('select mac from dhcp.hosts where mac = %s',(mac,))
        return cur.rowcount > 0
    finally:
        cur.close()

#funcion que agrega el host a la base
def addHost(con, ip, mac):
    cur = con.cursor()
    try:
        rid = str(uuid.uuid4())
        cur.execute('insert into dhcp.hosts (id, ip, mac) values (%s, %s, %s)', (rid, ip, mac))
    finally:
        cur.close()

leases = sys.argv[1]
conf = sys.argv[2]

f = open(leases, 'r')
f2 = open(conf, 'r')

set_mac = set()
set_hosts = set()

comment = False


try:
    #reviso linea por linea el archivo dhcpd.leases buscando hardware ethernet
    for line in f:
        if 'hardware ethernet' in line:
            #si existe guardo los caracteres de la mac
            mac = (line[20:-2])
            # y voy agregando las macs a set_mac
            set_mac.add(mac)
    #print(set_mac)
    print('--> CANTIDAD DE MACS EN EL LEASES  {}'.format(len(set_mac)))
finally:
    f.close()

#leasess de conexion
reg = inject.instance(Registry)
conn = Connection(reg.getRegistry('dcsys'))
con = conn.get()

try:
    net = '10.1.0.'
    ip = 0
    cant = 0
    for mac in set_mac:
        if isExist(con, mac):
            break
            #print('ya existe {}'.format(mac))
        else:
            print('no existe {}'.format(mac))
            ip+=1
            host = net + str(ip)
            addHost(con, host, mac)
            cant+=1
        con.commit()
    print('--> MACS AGREGADAS A LA BASE {}'.format(cant))
finally:
    conn.put(con)
print('--------------********************---------------------')

try:
    #reviso linia por linea el archivo dhcpd.conf buscando los hosts
    for line in f2:
        if 'host ' in line:
            if '#host ' in line:
                comment = True
                #print('host comentado {}'.format(line[:-3]))

            else:
                comment = False
                #si existe guardo los caracteres del nombre del host
                host = (line[5:-3])
                # y voy agregando los host a set_host
                set_hosts.add(host)

                print(host)

        if 'hardware ethernet' in line  and not comment:
            mac = (line[26:-2])
            print(mac)

        if 'fixed-address' in line  and not comment:
            ip = (line[22:-2])
            print(ip)

        #print('HOST {} MAC {} IP {}'.format(host, mac, ip))

    print('HOSTS {}'.format(len(set_hosts)))
finally:
    f2.close()
