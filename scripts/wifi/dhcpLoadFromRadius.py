
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
from model.users.users import User
from model.dhcp.dhcp import DhcpHost, DhcpNetwork, DhcpAssignation
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

def loadUserData(dnis):
    users = {}
    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        Connection.readOnly(con)
        userIds = User.findByDni(con, dnis)
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
    users = loadUserData(rad.keys())

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        # obtengo las redes y subredes
        networks = DhcpNetwork.findById(con, DhcpNetwork.findAll(con))
        wnets = {}
        for n in networks:
            wnets[n.id] = fce.wifiSubnets(n.ip)

        ''' genero aca las instancias para que sea un poco mas rapido el codigo '''
        net = DhcpNetwork()
        d = DhcpHost()
        da = DhcpAssignation()

        '''  asigno las ips para las macs que no tengan ya asignadas '''
        for dni in rad.keys():
            macs = rad[dni]
            for mac in macs:
                logging.info('mac : {}'.format(mac))

                ''' chequeo a ver en que redes no esta generada la mac '''
                toGenerate = []
                hids = DhcpHost.findByMac(con, mac)
                if len(hids) > 0:
                    hosts = DhcpHost.findById(con, hids)
                    for n in networks:
                        found = False
                        for h in hosts:
                            if n.includes(h):
                                found = True
                                ''' por las dudas que no tenga asignación, la genero '''
                                if dni in users:
                                    da.userId = users[dni].id
                                    da.hostId = h.id
                                    da.persist(con)
                                    con.commit()
                                break

                        if not found:
                            toGenerate.append(n)
                else:
                    toGenerate.extend(networks)

                ''' genero las ips en las redes faltantes '''
                for n in toGenerate:
                    if dni in autoridades:
                        net.ip = wnets[n.id]['authorities']
                    else:
                        net.ip = wnets[n.id]['general']

                    ip = net.findNextIpAvailable(con)
                    d.id = str(uuid.uuid4())
                    d.mac = mac
                    d.ip = ip
                    d.persist(con)

                    if dni in users:
                        da.userId = users[dni].id
                        da.hostId = d.id
                        da.persist(con)

                if len(toGenerate) > 0:
                    con.commit()






    finally:
        conn.put(con)
