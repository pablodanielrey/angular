
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
from model.dhcp import fce
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

    autoridades = [
        '24892148',     # pablo diaz
        '27294557',     # pablo rey
        '30057880',     # charly
        '31993212',     # adrian
        '25952190',     # julieta
        '13908434',     # laura catani
        '18283954',     # armengol
        '26578935',     # masson
        '26250165',     # eduardo degiusti
        '23454309',     # marina gs
        '20294338',     # diego felices
        '17755153',     # leo gasparini
        '22349070',     # mariana marchioni
        '29763750'     # paula beyries
    ]


    rad = loadRadiusRegs()
    #users = loadUserData()

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        # obtengo las redes y subredes
        networks = DhcpNetwork.findById(con, DhcpNetwork.findAll(con))
        wnets = {}
        for n in networks:
            wnets[n.id] = fce.wifiSubnets(n.ip)

        net = DhcpNetwork()
        # asigno las ips
        for dni in rad.keys():
            macs = rad[dni]
            for mac in macs:
                logging.info('mac : {}'.format(mac))
                for n in networks:
                    """
                        hack para hacerlo funcionar
                    """
                    if dni in autoridades:
                        net.ip = wnets[n.id]['authorities']
                    else:
                        net.ip = wnets[n.id]['general']

                    ip = net.findNextIpAvailable(con)
                    d = DhcpHost()
                    d.mac = mac
                    d.ip = ip
                    d.persist(con)
                con.commit()

    finally:
        conn.put(con)
