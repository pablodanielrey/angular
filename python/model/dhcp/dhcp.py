# -*- coding: utf-8 -*-

"""
    Se supone que se tiene la configuración del failOver dentro de failOver.conf
"""

import uuid
import inject
import logging
import ipaddress
from model.connection.connection import Connection
from model.dao import DAO


class DhcpAssignationDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        cur = con.cursor()
        try:
            cur.execute('create schema if not exists dhcp')

            cur.execute("""
                    create table if not exists dhcp.assignations (
                        user_id varchar not null references profile.users (id),
                        host_id varchar not null references dhcp.hosts (id)
                    )
                """)

        finally:
            cur.close()

    @classmethod
    def __fromResult(r):
        d = DhcpAssignation()
        d.hostId = r['host_id']
        d.userId = r['user_id']
        return d

    @classmethod
    def findByHost(cls, con, hostId):
        cur = con.cursor()
        try:
            cur.execute('select * from dhcp.assignations where host_id = %s', (hostId,))
            return [cls.__fromResult(r) for r in cur]

        finally:
            cur.close()

    @classmethod
    def findByUser(cls, con, userId):
        cur = con.cursor()
        try:
            cur.execute('select * from dhcp.assignations where user_id = %s', (userId,))
            return [cls.__fromResult(r) for r in cur]

        finally:
            cur.close()

    @classmethod
    def persist(cls, con, instance):
        cur = con.cursor()
        try:
            cur.execute('select * from dhcp.assignations where user_id = %(userId)s and host_id = %(hostId)s', instance.__dict__)
            if cur.rowcount <= 0:
                cur.execute('insert into dhcp.assignations (user_id, host_id) values (%(userId)s, %(hostId)s)', instance.__dict__)

        finally:
            cur.close()


class DhcpAssignation:

    dao = DhcpAssignationDAO

    def __init__(self):
        self.userId = None
        self.hostId = None

    def persist(self, con):
        self.dao.persist(con, self)

    @classmethod
    def findByHost(con, hostId):
        return self.dao.findByHost(con, hostId)

    @classmethod
    def findByUser(con, userId):
        return self.dao.findByUser(con, userId)


class DhcpHostDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        cur = con.cursor()
        try:
            cur.execute('create schema if not exists dhcp')

            cur.execute("""
                    create table if not exists dhcp.hosts (
                        id varchar primary key,
                        mac macaddr not null,
                        ip inet not null,
                        created timestamptz default now()
                    )
                """)

        finally:
            cur.close()

    @classmethod
    def __fromResult(cls, r):
        d = DhcpHost()
        d.id = r['id']
        d.ip = ipaddress.ip_interface(r['ip'])
        d.mac = r['mac']
        return d

    @classmethod
    def findById(cls, con, ids):
        cur = con.cursor()
        try:
            cur.execute('select * from dhcp.hosts where id in %s', (tuple(ids),))
            return [cls.__fromResult(c) for c in cur]

        finally:
            cur.close()

    @classmethod
    def findByIp(cls, con, ip):
        cur = con.cursor()
        try:
            cur.execute('select id from dhcp.hosts where ip = %s', (str(ip),))
            return [h['id'] for h in cur]

        finally:
            cur.close()

    @classmethod
    def findByMac(cls, con, mac):
        cur = con.cursor()
        try:
            cur.execute('select id from dhcp.hosts where mac = %s order by ip asc', (mac,))
            return [h['id'] for h in cur]

        finally:
            cur.close()

    @classmethod
    def findByNetwork(cls, con, networks):
        cur = con.cursor()
        try:
            ips = []
            for n in networks:
                cur.execute('select id from dhcp.hosts where ip << %s order by ip asc', (str(n),))
                ips.extend([h['id'] for h in cur])
            return ips

        finally:
            cur.close()

    @classmethod
    def findLastByNetwork(cls, con, network):
        cur = con.cursor()
        try:
            cur.execute('select id from dhcp.hosts where ip << %s order by ip desc limit 1', (str(network),))
            if cur.rowcount <= 0:
                return None
            return cur.fetchone()['id']

        finally:
            cur.close()

    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            cur.execute('select id from dhcp.hosts')
            return [h['id'] for h in cur]

        finally:
            cur.close()

    @classmethod
    def persist(cls, con, instance):
        cur = con.cursor()
        try:
            instance.ipaddress = str(instance.ip)
            cur.execute('insert into dhcp.hosts (id, mac, ip) values (%(id)s, %(mac)s, %(ipaddress)s)', instance.__dict__)

        finally:
            cur.close()


class DhcpNetworkDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        cur = con.cursor()
        try:
            cur.execute('create schema if not exists dhcp')

            cur.execute("""
                    create table if not exists dhcp.networks (
                        id varchar primary key,
                        name varchar default '',
                        ip cidr not null,
                        gateway inet not null,
                        range_init inet,
                        range_end inet
                    )
                """)
        finally:
            cur.close()

    @classmethod
    def persist(cls, con, instance):
        cur = con.cursor()
        try:
            d = instance.__dict__
            d['ipAddress'] = str(instance.ip)
            d['rangeInitAddress'] = str(instance.rangeInit)
            d['rangeEndAddress'] = str(instance.rangeEnd)
            d['gatewayAddress'] = str(instance.gateway)
            cur.execute('insert into dhcp.networks '
                        '(id, name, ip, range_init, range_end, gateway) values '
                        '(%(id)s, %(name)s, %(ipAddress)s, %(rangeInitAddress)s, %(rangeEndAddress)s, %(gatewayAddress)s)', instance.__dict__)

        finally:
            cur.close()

    @classmethod
    def __fromResult(cls, r):
        d = DhcpNetwork()
        d.id = r['id']
        d.name = r['name']
        d.ip = ipaddress.ip_network(r['ip'])
        d.rangeInit = ipaddress.ip_address(r['range_init'])
        d.rangeEnd = ipaddress.ip_address(r['range_end'])
        d.gateway = ipaddress.ip_address(r['gateway'])
        return d

    @classmethod
    def findById(cls, con, ids):
        cur = con.cursor()
        try:
            cur.execute('select * from dhcp.networks where id in %s', (tuple(ids),))
            return [cls.__fromResult(c) for c in cur]

        finally:
            cur.close()

    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            cur.execute('select id from dhcp.networks')
            return [n['id'] for n in cur]

        finally:
            cur.close()



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

    dao = DhcpHostDAO

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.mac = None
        self.ip = None

    @classmethod
    def findByNetwork(cls, con, networks):
        return cls.dao.findByNetwork(con, networks)

    @classmethod
    def findByMac(cls, con, mac):
        return cls.dao.findByMac(con, mac)

    @classmethod
    def findByIp(cls, con, ip):
        return cls.dao.findByIp(con, ip)

    @classmethod
    def findLastByNetwork(cls, con, network):
        return cls.dao.findLastByNetwork(con, network)

    @classmethod
    def findById(cls, con, ids):
        return cls.dao.findById(con, ids)

    @classmethod
    def findAll(cls, con):
        return cls.dao.findAll(con)

    def persist(self, con):
        return self.dao.persist(con, self)

    def toFile(self, f):
        f.write("""
            host {} {{
                hardware ethernet {};
                fixed-address {};
            }}
        """.format(
            self.id,
            self.mac,
            self.host
        ))


class DhcpNetwork:

    dao = DhcpNetworkDAO

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.name = None
        self.ip = None
        self.rangeInit = None
        self.rangeEnd = None
        self.gateway = None
        self.failOverName = 'fp'

    def toFile(self, f):
        f.write("""
            # {}
            subnet {} netmask {} {{
                option routers {};
                pool {{
                    failover peer "{}";
                    range {} {};
                }}
            }}
        """.format(
                self.name,
                self.ip,
                self.gateway,
                self.failOverName,
                self.rangeInit,
                self.rangeEnd
            ))

    def persist(self, con):
        return self.dao.persist(con, self)

    def findNextIpAvailable(self, con):
        last = DhcpHost.findById(con, [DhcpHost.findLastByNetwork(con, self.ip)])
        if len(last) <= 0:
            return self.ip[1]
        else:
            return last[0].ip + 1

    def includes(self, dhcpHost):
        return dhcpHost.ip in self.ip

    @classmethod
    def findById(cls, con, ids):
        return cls.dao.findById(con, ids)

    @classmethod
    def findAll(cls, con):
        return cls.dao.findAll(con)
