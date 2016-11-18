import uuid
import logging
import pytz
import sys
sys.path.append('../../python')

import inject
inject.configure()

from model.registry import Registry
from model.connection.connection import Connection

from model.dhcp.dhcp import DhcpHost, PublicIp
from model.dhcp import fce
import ipaddress


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    firewallFile = sys.argv[1]

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    rules = "#!/bin/bash\n"
    try:
        publics = PublicIp.findById(con, PublicIp.findAll(con))
        for public in publics:
            # obtengo las ip privada relacionada a esa ip publica
            hosts = DhcpHost.findById(con, DhcpHost.findByMac(con, public.mac))
            if len(hosts) <= 0:
                continue

            rules = rules + "iptables -A FORWARD -d {} -j ACCEPT\n".format(str(public.ip.ip))
            rules = rules + "iptables -A FORWARD -d {} -j ACCEPT\n".format(str(hosts[0].ip.ip))
            for h in hosts:
                if public.redirectNetwork is not None and h.ip.ip in public.redirectNetwork:
                    rules = rules + "iptables -t nat -A PREROUTING -d {} -m state --state NEW -j DNAT --to-destination {} \n".format(str(public.ip.ip), str(h.ip.ip))
                rules = rules + "iptables -t nat -A POSTROUTING -s {} -j SNAT --to-source {} \n".format(str(h.ip.ip), str(public.ip.ip))
            rules = rules + "\n"

    finally:
        conn.put(con)

    with open(firewallFile,'w') as f:
        f.write(rules)
