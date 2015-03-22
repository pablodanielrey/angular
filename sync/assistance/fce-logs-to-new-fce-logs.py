# -*- coding: utf-8 -*-
import ldap3
import psycopg2
import datetime, pytz
import sys

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

    print(len(rdata))

    return rdata



def copyLogs(src,dst,personCache):

    cdst = dst.cursor()

    csrc = src.cursor()
    csrc.execute('select id,person_id,verifymode,date from attlog order by date asc')

    count = 0
    for sl in csrc:
        count = count + 1

        cdst.execute('select id from assistance.attlog where id = %s',(sl[0],))
        if cdst.rowcount > 0:
            print("{0} log ya importado asi que lo ignoro".format(count))
            continue

        date = sl[3]

        tz = pytz.timezone("America/Buenos_Aires")
        local = tz.localize(date)
        utcdate = local.astimezone(pytz.utc)

        personId = sl[1]
        if personId not in personCache:
            print("la persona {0} no existe en la cache".format(personId))
            continue

        dni = personCache[personId]

        cdst.execute('select id from profile.users where dni = %s',(dni,))
        person = cdst.fetchone()
        if (person == None):
            print("no se encuentra persona con dni = {0}".format(dni))
            continue

        personId = person[0]

        print("{4} insertando para {0} {1} -- {2} | utc={3}".format(personId,dni,date,utcdate,count))
        req = (sl[0],'1c5c90a3-2873-4b8f-9931-faca5808e932',personId,sl[2],utcdate)
        cdst.execute('insert into assistance.attlog (id,device_id,user_id,verifymode,log) values (%s,%s,%s,%s,%s)',req)


if __name__ == '__main__':

    """
        argumentos ej :
        python3 fce-logs-to-new-fce-logs.py 127.0.0.1 3389 admin pas 127.0.0.1 8181 dbuser dbpass db 127.0.0.1 5432 dbuser dbpass db2
    """

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


    personCache = makeUsersCache(lhost,int(lport),luser,lpassw)

    src = psycopg2.connect(host=shost, port=sport, user=suser, password=spassw, dbname=sdb)
    dst = psycopg2.connect(host=dhost, port=dport, user=duser, password=dpassw, dbname=ddb)

    copyLogs(src,dst,personCache)

    dst.commit()

    src.close()
    dst.close()
