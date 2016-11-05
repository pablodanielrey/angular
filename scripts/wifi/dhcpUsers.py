
import pymysql
import pymysql.cursors

import json
import datetime
import pytz
from dateutil.tz import tzlocal
import dateutil
import sys
sys.path.append('../../python')

import inject
inject.configure()

import uuid
import logging

from model.registry import Registry
from model.connection.connection import Connection
from model.offices.office import Office
from model.users.users import User, UserPassword



class Iph:

    def __init__(self, b):
        self.base = b
        self.count = 1
        self.macs = []
        self.networks = ['10.10','10.17','10.26','10.14','10.8','10.9','10.11','10.15','10.12','10.18','10.19','10.20']

    def __getIp(self, n):
        return '.{}.{}'.format((n // 254) + self.base, (n % 254) + 1)

    def getIps(self, mac):
        ''' obtiene las ips de las redes asignadas para determinada mac '''
        if mac in self.macs:
            return []
        self.macs.append(mac)
        ips = []
        ip = self.__getIp(self.count)
        for n in self.networks:
            ips.append('{}{}'.format(n, ip))
        self.count = self.count + 1
        return ips

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    # obtengo los registros de acceso de los aps
    logging.info('obtieniendo registros de logs')
    mcon = pymysql.connect(host='163.10.17.130',
                    user='freeradius',
                    password='radacct',
                    db='freeradius',
                    cursorclass=pymysql.cursors.DictCursor)
    try:
        macs = {}
        with mcon.cursor() as cur:
            cur.execute('select distinct username, callingstationid from radacct order by username')
            for r in cur:
                mac = r['callingstationid'].replace('-',':')
                dni = r['username']
                if dni not in macs:
                    macs[dni] = set()
                macs[dni].add(mac)
    finally:
        mcon.close()
    logging.info('{} registros obtenidos'.format(len(macs.keys())))

    logging.info('Obteniendo usuarios')
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

    print('Usuarios obtenidos: {}'.format(len(users.keys())))


    ## creo los generadores de ips para los distintos rangos.
    ipa = Iph(250)      # 10.250.x.x -----> autoridades
    ipd = Iph(100)      # >= 10.100.x.x --> docentes
    ipn = Iph(10)       # >= 10.10.x.x ---> alumnos

    # registro usuarios que son autoridades
    autoridades = [
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
        '29763750'      # paula beyries
    ]

    logging.info('escribiendo los archivos dhcp')
    with open('/tmp/dhcp-alumnos.txt','w') as dalumnos:
        with open('/tmp/dhcp-docentes.txt','w') as ddocentes:
            with open('/tmp/dhcp-autoridades.txt','w') as dautoridades:
                for dni in macs:
                    maccs = macs[dni]
                    ips = []

                    fileToWrite = None
                    if dni in autoridades:
                        fileToWrite = dautoridades
                        for mac in maccs:
                            ips.extend(ipa.getIps(mac))

                    elif dni in users and users[dni].type == 'teacher':
                        fileToWrite = ddocentes
                        for mac in maccs:
                            ips.extend(ipd.getIps(mac))

                    else:
                        fileToWrite = dalumnos
                        for mac in maccs:
                            ips.extend(ipn.getIps(mac))

                    name = users[dni].name if dni in users and users[dni].name is not None else 'no tiene'
                    lastname = users[dni].lastname if dni in users and users[dni].lastname is not None else 'no tiene'

                    for ip in ips:
                        hname = str(uuid.uuid4())
                        fileToWrite.write("""
                                # {} {} {}
                                host {} {{
                                    hardware ethernet {};
                                    fixed-address {};
                                }}\n
                        """.format(dni, name, lastname, hname, mac, ip))

    sys.exit(1)


    import re
    r = re.compile('[a-zA-Z\d]+')

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        userIds = User.findAll(con)
        users = []
        for uid in [i for (i, v) in userIds]:
            user = User.findById(con, [uid])[0]
            if user.type != 'student':
                users.extend(UserPassword.findByUserId(con, uid))

        with open('/etc/freeradius/radius-users', 'w') as f:
            for up in users:
                if r.match(up.username) is None or ' ' in up.username:
                    continue

                f.write("""

{} Cleartext-Password := "{}"
    Service-Type = Framed-User,
    Framed-Protocol = PPP,
    Framed-Compression = Van-Jacobsen-TCP-IP
                """.format(up.username, up.password))

    finally:
        conn.put(con)
