
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

def subnets(network):
    """
        Genero las subredes especificadas de acuerdo a la política de la facultad
    """
    n = ipaddress.ip_network(network + '.0.0/16')
    subn = list(n.subnets(new_prefix=17))
    general = subn[0]
    subn = list(subn[1].subnets(new_prefix=19))
    authorities = subn[0]
    events = subn[1]
    voip = subn[2]
    admin = subn[3]
    dynamic = list(subn[3].subnets(new_prefix=26))[0]

    return {
        'network': n,
        'general': general,
        'authorities': authorities,
        'events': events,
        'voip': voip,
        'admin': admin,
        'dynamic': dynamic
    }

def combine(ip, network):
    """ retorna una interface a partir de una ip y una red """
    return ipaddress.ip_interface(str(ip) + '/' + str(network.prefixlen))


networks = ['10.10','10.17','10.26','10.14','10.8','10.9','10.11','10.15','10.12','10.18','10.19','10.20']

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        for n in networks:
            netww = subnets(n)
            dn = DhcpNetwork()
            dn.ip = netww['network']
            dn.gateway = combine(dn.ip.broadcast_address - 1, dn.ip)
            dn.rangeInit = combine(netww['dynamic'].network_address + 1, netww['dynamic'])
            dn.rangeEnd = combine(netww['dynamic'].broadcast_address - 1, netww['dynamic'])
            dn.persist(con)

        con.commit()

    finally:
        conn.put(con)
