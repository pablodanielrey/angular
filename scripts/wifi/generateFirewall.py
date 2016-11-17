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

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        publics = PublicIp.findById(con, PublicIp.findAll(con))
        rules = ""
        for public in publics:
            # obtengo las ip privada relacionada a esa ip publica
            hosts = DhcpHost.findById(con, DhcpHost.findByMac(con, public.mac))
            if len(hosts) <= 0:
                continue

            rules = rules + "iptables -t nat -A PREROUTING -d {} -m state --state NEW -j DNAT --to-destination {} \n".format(str(public.ip.ip), str(hosts[0].ip.ip))
            for h in hosts:
                rules = rules + "iptables -t nat -A POSTROUTING -s {} -j SNAT --to-source {} \n".format(str(h.ip.ip), str(public.ip.ip))
        print(rules)

    finally:
        conn.put(con)


"""
ips publicas de videoconferencia: 163.10.17.131, 163.10.17.132, 163.10.17.133
"""
#  hardware ethernet 38:60:77:05:51:3B;
#  fixed-address 10.11.1.1;

#host videoconferencia-prueba {
#  hardware ethernet 50:32:75:a1:1e:f9;
#  fixed-address 10.100.1.253;
#}
