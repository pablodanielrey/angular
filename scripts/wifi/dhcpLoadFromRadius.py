
import pymysql
import pymysql.cursors

import uuid
import logging
import json
import datetime
import pytz
from dateutil.tz import tzlocal
import dateutil
import sys
sys.path.append('../../python')

import inject
inject.configure()

from model.registry import Registry
from model.connection.connection import Connection

from model.dhcp.dhcp import DhcpHost, DhcpNetwork
import ipaddress

def loadRadiusRegs():
    macs = {}
    mcon = pymysql.connect(host='163.10.17.130',
                    user='freeradius',
                    password='radacct',
                    db='freeradius',
                    cursorclass=pymysql.cursors.DictCursor)
    try:
        with mcon.cursor() as cur:
            cur.execute('select distinct username, callingstationid from radacct order by username')
            for r in cur:
                mac = r['callingstationid'].replace('-',':').upper()
                dni = r['username']
                if dni not in macs:
                    macs[dni] = set()
                macs[dni].add(mac)
    finally:
        mcon.close()
    return macs

def loadUserData():
    users = {}
    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        Connection.readOnly(con)
        userIds = User.findByDni(con, macs.keys())
        userss = User.findById(con, [i for (i,v) in userIds])
        for u in userss:
            users[u.dni] = u
    finally:
        conn.put(con)
    return users

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    rad = loadRadiusRegs()
    #users = loadUserData()

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        netww = {}
        networks = DhcpNetwork.findById(con, DhcpNetwork.findAll(con))
        for n in networks:
            count = 10
            for macs in rad.values():
                for mac in macs:
                    d = DhcpHost()
                    d.mac = mac
                    d.ip = ipaddress.ip_interface(str(n.ip[count]) + '/' + str(n.ip.prefixlen))
                    logging.info('Agregando {}'.format(d.ip))
                    d.persist(con)
                    count = count + 1

        con.commit()

    finally:
        conn.put(con)
