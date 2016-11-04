
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

def getIp(b, n):
    return '.{}.{}'.format((n // 250) + b, (n % 250) + 1)

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    # obtengo todos los usuasrios para referenciarlos despues con los registros de acceso.

    users = {}

    print('Obteniendo usuarios')

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        Connection.readOnly(con)
        userIds = User.findAll(con)
        for uid in [i for (i, v) in userIds]:
            user = User.findById(con, [uid])[0]
            users[user.dni] = user

    finally:
        conn.put(con)


    print('Usuarios obtenidos: {}'.format(len(users.keys())))


    ## las redes a generar:

    networks = ['10.10','10.17','10.26','10.14','10.8','10.9','10.11','10.15','10.12','10.18','10.19','10.20']
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

    # obteniendo los registros de acceso.

    mcon = pymysql.connect(host='163.10.17.130',
                    user='freeradius',
                    password='radacct',
                    db='freeradius',
                    cursorclass=pymysql.cursors.DictCursor)
    try:
        with open('/tmp/dhcp-alumnos.txt','w') as dalumnos:
            with open('/tmp/dhcp-docentes.txt','w') as ddocentes:
                with open('/tmp/dhcp-autoridades.txt','w') as dautoridades:
                    with mcon.cursor() as cur:
                        cur.execute('select distinct username, callingstationid from radacct order by username')

                        #contador y base de cada uno de los grupos de usuarios. autoridades, docentes, alumnos
                        ipa = 1
                        basea = 250

                        ipd = 1
                        based = 100

                        ipn = 1
                        basen = 1

                        macsProcessed = []

                        for r in cur:
                            tipo = 'n'

                            mac = r['callingstationid'].replace('-',':')
                            if mac in macsProcessed:
                                continue

                            macsProcessed.append(mac)

                            dni = r['username']
                            username = ' no tiene '
                            lastname = ' no tiene '
                            try:
                                uname = users[dni].name
                                lastname = users[dni].lastname
                                tipo = 'd' if users[dni].type == 'teacher' else 'n'
                                tipo = 'a' if dni in autoridades else tipo
                            except Exception as e:
                                pass

                            #net = r['calledstationid'].split(':')[1]
                            #ap = r['calledstationid'].split(':')[0]
                            name = str(uuid.uuid4())

                            for ne in networks:

                                fileToWrite = None
                                ip = ''

                                if tipo == 'a':
                                    ip = getIp(basea, ipa)
                                    fileToWrite = dautoridades

                                elif tipo == 'd':
                                    ip = getIp(based, ipd)
                                    fileToWrite = ddocentes

                                elif tipo == 'n':
                                    ip = getIp(basen, ipn)
                                    fileToWrite = dalumnos

                                fileToWrite.write("""
                                        # {} {} {}
                                        host {} {{
                                            hardware ethernet {};
                                            fixed-address {}{};
                                        }}\n
                                """.format(dni, uname, lastname, name, mac, ne, ip))

                            if tipo == 'a':
                                ipa = ipa + 1

                            if tipo == 'd':
                                ipd = ipd + 1

                            if tipo == 'n':
                                ipn = ipn + 1


    finally:
        mcon.close()

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
