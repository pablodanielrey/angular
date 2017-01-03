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
                l = r[1]
                n = r[1]
                if ',' in r[1]:
                    l = r[1].split(',')[0].strip()
                    n = r[1].split(',')[1].strip()
                leg = r[2].strip()
                d = r[3].upper().replace('DNT','').replace('CI','').replace('DNI','').replace('PAS','').replace('.','').strip()
                print('a:{} n:{} d:{}'.format(l,n,d))
                uid = None
                cur.execute('select id from profile.users where dni = %s', (d,))
                if cur.rowcount <= 0:
                    uid = str(uuid.uuid4())
                    cur.execute('insert into profile.users (id, name, lastname, dni, type) values (%s,%s,%s,%s,%s)',(uid, n, l, d, 'student'))
                    cur.execute('insert into credentials.user_password (id, user_id, username, password) values (%s,%s,%s,%s)',(str(uuid.uuid4()), uid, d, d))
                else:
                    uid = cur.fetchall()[0][0]

                try:
                    cur.execute('select id from students.users where id = %s', (uid,))
                    if cur.rowcount > 0:
                        continue

                    cur.execute('select id from students.users where student_number = %s', (leg,))
                    if cur.rowcount > 0:
                        print('ya existe el legajo : {}'.format(leg))
                        continue

                    cur.execute('insert into students.users (id, student_number, condition) values (%s, %s, %s)', (uid, leg, 'ingreso2017'))
                finally:
                    print('ya tiene legago : {}'.format(uid))

    finally:
        cur.close()
        con.commit()
finally:
    con.close()
