import psycopg2
import sys
import re
import uuid
import csv

host = sys.argv[1]
user = sys.argv[2]
passw = sys.argv[3]
arch = sys.argv[4]

con = psycopg2.connect('host={} dbname={} user={} password={}'.format(host, 'dcsys', user, passw))
try:
    cur = con.cursor()
    try:
        with open(arch,'r') as f:
            sr = csv.reader(f, delimiter=';', quotechar='"')
            for r in sr:
                l = r[0].split(',')[0].strip()
                n = r[0].split(',')[1].strip()
                d = r[1].upper().replace('DNT','').replace('CI','').replace('DNI','').replace('PAS','').replace('.','').strip()
                print('a:{} n:{} d:{}'.format(l,n,d))
                uid = str(uuid.uuid4())
                cur.execute('select id from profile.users where dni = %s', (d,))
                if cur.rowcount > 0:
                    print('recursante')
                    continue
                cur.execute('insert into profile.users (id, name, lastname, dni, type) values (%s,%s,%s,%s,%s)',(uid, n, l, d, 'student'))
                cur.execute('insert into credentials.user_password (id, user_id, username, password) values (%s,%s,%s,%s)',(str(uuid.uuid4()), uid, d, d))
    finally:
        cur.close()
        con.commit()
finally:
    con.close()
