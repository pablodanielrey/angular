import pytz
import sys
sys.path.append('../../python')

import inject
inject.configure()

import logging
import uuid

from model.registry import Registry
from model.connection.connection import Connection

from model.dhcp.dhcp import DhcpHost, DhcpNetwork, DhcpManual
from model.dhcp import fce
import ipaddress


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    leases = sys.argv[1]

    f = open(leases, 'r')

    macs = set()

    try:
        for line in f:
            if 'hardware ethernet' in line:
                mac = (line[20:-2])
                macs.add(mac)
    finally:
        f.close()

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

        for mac in macs:
            logging.info('leyendo mac : {} '.format(mac))

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
                            break
                    if not found:
                        toGenerate.append(n)
            else:
                toGenerate.extend(networks)

            ''' genero las ips en las redes faltantes '''
            for n in toGenerate:
                net.ip = wnets[n.id]['general']

                ip = net.findNextIpAvailable(con)
                d.id = str(uuid.uuid4())
                d.mac = mac
                d.ip = ip
                d.persist(con)
                logging.info('mac: {} ip: {}'.format(d.mac, d.ip))

            con.commit()

    finally:
        conn.put(con)
