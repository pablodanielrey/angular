# -*- coding: utf-8 -*-

import csv, sys
import psycopg2
import uuid

host = sys.argv[1]
port = sys.argv[2]
db = sys.argv[3]
user = sys.argv[4]
passw = sys.argv[5]

con = psycopg2.connect(host=host, port=port, user=user, password=passw, dbname=db)
cur = con.cursor()

for app,func,nombre,dni,maili,e,s,of,cargo,ma in csv.reader(sys.stdin):
    if dni == None or dni == '':
        continue

    pid = str(uuid.uuid4())
    cur.execute('select dni from profile.users where dni = %s', (dni,))
    if cur.rowcount > 0:
        print("{0} ya existe".format(dni))
        continue

    cur.execute('insert into profile.users (id,dni,name,lastname) values (%s,%s,%s,%s)', (pid,dni,nombre,app))

con.commit()
con.close()
