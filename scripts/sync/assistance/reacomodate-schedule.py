# -*- coding: utf-8 -*-

import csv, sys, pytz, datetime
import psycopg2
from dateutil.relativedelta import relativedelta
import uuid, calendar
import logging
import re
import time


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


    con = psycopg2.connect(host=host, port=port, user=user, password=passw, dbname=db)
    cur = con.cursor()
    cur.execute("set time zone %s",('utc',))

    s = datetime.datetime(year=2015,month=2,day=24)
    cur.execute('select user_id from assistance.schedule where date::date = %s group by user_id',(s,))
    users = cur.fetchall()
    for userr in users:
        user = userr[0]
        cur.execute('select id,date,sstart,send from assistance.schedule where date::date = %s and user_id = %s',(s,user))
        data = cur.fetchall()
        if len(data) > 1:
            first = True
            days = 2
            for id,date,sstart,send in data:
                if first:
                    first = False
                    continue
                logging.debug('{}, {}, {}, {}'.format(id,date,sstart,send))
                ndate = date + relativedelta(days=days)
                nstart = sstart + relativedelta(days=days)
                nend = send + relativedelta(days=days)
                logging.debug('{}, {}, {}, {}'.format(id,ndate,nstart,nend))
                cur.execute('update assistance.schedule set date = %s, sstart = %s, send = %s where id = %s',(ndate,nstart,nend,id))
                days = days + 1
            con.commit()

    con.close()
