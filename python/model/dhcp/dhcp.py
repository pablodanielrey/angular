# -*- coding: utf-8 -*-

"""
    Se supone que se tiene la configuración del failOver dentro de failOver.conf
"""

import uuid
import inject
from model.connection.connection import Connection


class Dhcp:

    def __init__(self):
        self.maxLeaseTime = 7200
        self.defaultLeaseTime = 600
        self.domainName = 'econo.unlp.edu.ar'
        self.domainNameServers = ['163.10.17.4', '163.10.17.17']
        self.networks = []
        self.hosts = []

    def toFile(self, f):
        f.write("""
            ddns-update-style-none;
            default-lease-time {};
            max-lease-time {};
            option domain-name "{}";
            option domain-name-servers {};

            include "/etc/dhcp/failover.conf";


        """.format(
                self.defaultLeaseTime,
                self.maxLeaseTime,
                self.domainName,
                ', '.join(self.domainNameServers)
        ))

        for n in self.networks:
            n.toFile(f)

        for h in self.hosts:
            h.toFile(f)


class DhcpHost:

    def __init__(self):
        self.hostname = str(uuid.uuid4())
        self.mac = None
        self.ip = None

    @classmethod
    def __fromResult(cls, r):
        d = cls()
        d.mac = r['host']
        d.ip = r['ip']
        return d

    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            cur.execute('select * from dhcp.hosts')
            return [cls.__fromResult(c) for c in cur]

        finally:
            cur.close()

    def toFrite(self, f):
        f.write("""
            host {} {{
                hardware ethernet {};
                fixed-address {};
            }}
        """.format(
            self.hostname,
            self.mac,
            self.ip
        ))


class DhcpNetwork:

    def __init__(self):
        self.name = None
        self.ip = None
        self.netmask = None
        self.rangeInit = None
        self.rangeEnd = None
        self.gateway = None
        self.failOverName = 'fp'

    def toFile(self, f):
        f.write("""
            subnet {} netmask {} {{
                option routers {};
                pool {{
                    failover peer "{}";
                    range {} {};
                }}
            }}
        """.format(
                self.ip,
                self.netmask,
                self.gateway,
                self.failOverName,
                self.rangeInit,
                self.rangeEnd
            ))

    @classmethod
    def __fromResult(cls, r):
        d = cls()
        d.name = r['name']
        d.ip = r['ip']
        d.netmask = r['netmask']
        d.rangeInit = r['rangeInit']
        d.rangeEnd = r['rangeEnd']
        d.gateway = r['gateway']
        return d

    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            cur.execute('select * from dhcp.networks')
            return [cls.__fromResult(c) for c in cur]

        finally:
            cur.close()
