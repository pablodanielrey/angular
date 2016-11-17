import uuid
import logging
import pytz
import sys
sys.path.append('../../python')

import inject
inject.configure()

from model.registry import Registry
from model.connection.connection import Connection

from model.dhcp.dhcp import DhcpHost, DhcpNetwork, DhcpAssignation, DhcpManual
from model.dhcp import fce
import ipaddress


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        # obtengo las redes y subredes
        networks = DhcpNetwork.findById(con, DhcpNetwork.findAll(con))
        wnets = {}
        for n in networks:
            wnets[n.id] = fce.wifiSubnets(n.ip)

        # obtengo los aps
        aps = DhcpManual.findById(con, DhcpManual.findAll(con))

        ''' genero aca las instancias para que sea un poco mas rapido el codigo '''
        net = DhcpNetwork()
        d = DhcpHost()

        for ap in aps:
            logging.info('mac : {} description: {}'.format(ap.mac, ap.description))

            ''' chequeo a ver en que redes no esta generada la mac '''
            toGenerate = []
            hids = DhcpHost.findByMac(con, ap.mac)

            if len(hids) > 0:
                hosts = DhcpHost.findById(con, hids)
                for n in networks:
                    found = False
                    for h in hosts:
                        if n.includes(h):
                            found = True
                            break
                    if not found:
                        logging.info("Agregando la red {}".format(n.ip))
                        toGenerate.append(n)
            else:
                toGenerate.extend(networks)

            ''' genero las ips en las redes faltantes '''
            for n in toGenerate:
                net.ip = wnets[n.id][ap.net]

                ip = net.findNextIpAvailable(con)
                d.id = str(uuid.uuid4())
                d.mac = ap.mac
                d.ip = ip
                d.persist(con)
                logging.info('mac: {} ip: {}'.format(d.mac, d.ip))


        con.commit()

    finally:
        conn.put(con)
