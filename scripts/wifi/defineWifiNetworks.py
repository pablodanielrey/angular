
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

from model.dhcp import fce
from model.dhcp.dhcp import DhcpHost, DhcpNetwork
import ipaddress

"""
    Las redes wifi dentro de económicas están divididas en:

        10.x.0.0/17 ----> alumnos y accesos normales
        10.x.128.0/19 --> autoridades
        10.x.160.0/19 --> eventos
        10.x.192.0/19 --> video conferencias
        10.x.224.0/19 --> systemas admin
            10.x.224.0/26 ---> rango dinámico provisorio (10.x.224.1 -- 10.x.224.62)

    estas subredes valen a la hora de asignar ips fijas a macs y polítias de firewall.
    para el ruteo se hace suppernetting a la 10.x.0.0/16
    el gateway siempre es la ultima de la red.

        10.x.255.254 -- gateway

"""

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        for n in fce.wifiNetworks():
            netww = fce.wifiSubnets(n)
            r = fce.wifiDynamicRange(netww)

            dn = DhcpNetwork()
            dn.ip = netww['network']
            dn.gateway = fce.gateway(dn.ip)
            dn.rangeInit = r['start']
            dn.rangeEnd = r['end']
            dn.persist(con)

        con.commit()

    finally:
        conn.put(con)
