# -*- coding: utf-8 -*-
import ldap3
import psycopg2
import datetime, pytz
import sys, logging

""" creo una cache de uuid --> dni """
def makeUsersCache(host,port,user,passw):

    s = ldap3.Server(host,port=port,get_info = ldap3.GET_ALL_INFO)
    c = ldap3.Connection(s,auto_bind = True, client_strategy = ldap3.STRATEGY_SYNC,user=user,password=passw)

    rdata = {}
    c.search("dc=econo","(x-dcsys-dni=*)",ldap3.SEARCH_SCOPE_WHOLE_SUBTREE, attributes = ['x-dcsys-uuid','x-dcsys-dni'])
    data = c.response
    for ob in data:
        attrs = ob['attributes']
        rdata[attrs['x-dcsys-uuid'][0]] = attrs['x-dcsys-dni'][0]

    c.unbind()

    logging.info('cantidad de personas leídas {}'.format(len(rdata)))

    return rdata



def copyLogs(src,dst,personCache):

    cdst = dst.cursor()
    cdst.execute("set timezone to 'UTC'")

    csrc = src.cursor()
    csrc.execute('select id,person_id,verifymode,date from attlog order by date asc')

    personsNot2 = 0
    personsNot = 0
    existent = 0
    count = 0
    for sl in csrc:
        count = count + 1

        cdst.execute('select id from assistance.attlog where id = %s',(sl[0],))
        if cdst.rowcount > 0:
            existent = existent + 1
            logging.debug("{0} log ya importado asi que lo ignoro".format(count))
            continue

        date = sl[3]

        tz = pytz.timezone("America/Buenos_Aires")
        local = tz.localize(date)
        utcdate = local.astimezone(pytz.utc)

        personId = sl[1]
        if personId not in personCache:
            logging.warn("la persona {0} no existe en la cache".format(personId))
            personsNot = personsNot + 1
            continue

        dni = personCache[personId]

        cdst.execute('select id from profile.users where dni = %s',(dni,))
        person = cdst.fetchone()
        if (person == None):
            logging.warn("no se encuentra persona con dni = {0}".format(dni))
            personsNot2 = personsNot2 + 1
            continue

        personId = person[0]

        cdst.execute('select id from assistance.attlog where log = %s',(utcdate,))
        if cdst.rowcount > 0:
            logging.debug("{4} ya existe {0} {1} -- {2} | utc={3}".format(personId,dni,date,utcdate,count))
            existent = existent + 1
        else:
            logging.debug("{4} insertando para {0} {1} -- {2} | utc={3}".format(personId,dni,date,utcdate,count))
            req = (sl[0],'1c5c90a3-2873-4b8f-9931-faca5808e932',personId,sl[2],utcdate)
            cdst.execute('insert into assistance.attlog (id,device_id,user_id,verifymode,log) values (%s,%s,%s,%s,%s)',req)
            dst.commit()


    logging.info('Cantidad de logs procesados : {}'.format(count))
    logging.info('Cantidad de logs existentes : {}'.format(existent))
    logging.info('Cantidad de logs con personas no existentes en cache : {}'.format(personsNot))
    logging.info('Cantidad de logs con personas no existentes en base destino : {}'.format(personsNot2))


if __name__ == '__main__':

    """
        argumentos ej :
        python3 fce-logs-to-new-fce-logs.py 127.0.0.1 3389 admin pas 127.0.0.1 8181 dbuser dbpass db 127.0.0.1 5432 dbuser dbpass db2
    """

    if len(sys.argv) < 15:
        logging.info('faltan argumentos')
        logging.info('python3 {} host-ldap port-ldap admin-ldap pass-ldap host-db-origen port-db-origen db-origen-user db-origen-pass db-orgien host-db-destino port-db-destino db-user-destino db-pass-destino db-destino'.format(sys.argv[0]))
        logging.info('')
        logging.info('Normalmente puede redireccionar puertos usando ssh y llamar al script usando parametros y puertos ya definidos')
        logging.info('Ej:')
        logging.info('ssh -L 3389:127.0.0.1:389 root@ldap; ssh -L 8181:127.0.0.1:5432 root@postgres-origen')
        logging.info('python3 {} 127.0.0.1 3389 admin pas 127.0.0.1 8181 dbuser dbpass db 127.0.0.1 5432 dbuser dbpass db2'.format(sys.argv[0]))
        sys.exit(1)

    lhost = sys.argv[1]
    lport = sys.argv[2]
    luser = sys.argv[3]
    lpassw = sys.argv[4]

    shost = sys.argv[5]
    sport = sys.argv[6]
    suser = sys.argv[7]
    spassw = sys.argv[8]
    sdb = sys.argv[9]

    dhost = sys.argv[10]
    dport = sys.argv[11]
    duser = sys.argv[12]
    dpassw = sys.argv[13]
    ddb = sys.argv[14]

    logging.basicConfig(filename='/tmp/copy-logs.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.INFO)

    logging.info('generando cache de personas')
    personCache = makeUsersCache(lhost,int(lport),luser,lpassw)

    logging.info('conectandose a las bases')
    src = psycopg2.connect(host=shost, port=sport, user=suser, password=spassw, dbname=sdb)
    dst = psycopg2.connect(host=dhost, port=dport, user=duser, password=dpassw, dbname=ddb)

    logging.info('copiando logs')
    copyLogs(src,dst,personCache)

    dst.commit()

    src.close()
    dst.close()
