# -*- coding: utf-8 -*-

import csv, sys, pytz, datetime
import psycopg2
from dateutil import parser
import uuid, calendar
import logging
import re
import time


def localice(date):
    if date.tzinfo is not None:
        return date
    timezone = "America/Buenos_Aires"
    tz = pytz.timezone(timezone)
    local = tz.localize(date)
    return local

def replaceTime(date,time):
    return date.replace(hour=time.hour,minute=time.minute,second=0,microsecond=0)



def getNumber(comp):
    if comp is None:
        comp = 0

    if comp is not None:
        try:
            comp = int(comp)
        except Exception as e:
            comp = 0

    return comp



if __name__ == '__main__':


    if len(sys.argv) < 6:
        print('debe invocar el script con los siguientes parámetros :')
        print('cat archivo.csv | python {} host port db user pass'.format(sys.argv[0]))
        sys.exit(1)


    #logging.basicConfig(filename='/tmp/import-schedule.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

    host = sys.argv[1]
    port = sys.argv[2]
    db = sys.argv[3]
    user = sys.argv[4]
    passw = sys.argv[5]



    date = datetime.datetime.now()
    dates = calendar.Calendar().monthdatescalendar(date.year,1)
    firstWeek = dates[0][:7]

    con = psycopg2.connect(host=host, port=port, user=user, password=passw, dbname=db)
    cur = con.cursor()
    cur.execute("set time zone %s",('utc',))

    #cur.execute('delete from assistance.schedule')

    logging.basicConfig(level=logging.DEBUG)

    title = False

    for line in csv.reader(sys.stdin):

        if not title:
            title = True
            continue

        logging.debug(line)

        nombre,app,dni,comp,lic,res = line

        if dni == None or dni == '':
            logging.warn('ignorando {} ya que no tiene dni'.format(line))
            continue

        cur.execute('select id,dni from profile.users where dni = %s', (dni,))
        if cur.rowcount <= 0:
            logging.warn('ignorando ya que no existe el dni {}'.format(dni))
            continue


        pid = cur.fetchone()[0]

        comp = getNumber(comp)
        lic = getNumber(lic)
        res = getNumber(res)

        fecha = datetime.datetime.now().replace(year=2015,month=1,day=1)

        logging.info('{} {} {} {} {}'.format(pid,fecha,comp,lic,res))

        req = ('48773fd7-8502-4079-8ad5-963618abe725',pid,comp,fecha)
        cur.execute('insert into assistance.justifications_stock (justification_id,user_id,stock,calculated) values (%s,%s,%s,%s)',req)

        req = ('76bc064a-e8bf-4aa3-9f51-a3c4483a729a',pid,lic,fecha)
        cur.execute('insert into assistance.justifications_stock (justification_id,user_id,stock,calculated) values (%s,%s,%s,%s)',req)

        if res > 0:
            req = ('50998530-10dd-4d68-8b4a-a4b7a87f3972',pid,res,fecha)
            cur.execute('insert into assistance.justifications_stock (justification_id,user_id,stock,calculated) values (%s,%s,%s,%s)',req)

    con.commit();
    con.close()
