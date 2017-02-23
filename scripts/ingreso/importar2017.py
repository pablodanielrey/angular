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
                nombres = r[0].split(',')
                a = nombres[0]
                n = nombres[0]
                if len(nombres) > 1:
                    a = nombres[0].strip()
                    n = nombres[1].strip()
                leg = r[1].strip()
                d = r[2].upper().replace('DNT','').replace('CI','').replace('DNI','').replace('PAS','').replace('.','').strip()
                print('a:{} n:{} d:{} l:{}'.format(a,n,d,leg))
                uid = str(uuid.uuid4())
                cur.execute('select id from profile.users where dni = %s', (d,))
                if cur.rowcount > 0:
                    print('recursante')
                    continue
                cur.execute('select id from students.users where student_number = %s', (leg,))
                if cur.rowcount > 0:
                    print('ya existe ese legajo')
                    continue
                cur.execute('insert into profile.users (id, name, lastname, dni, type) values (%s,%s,%s,%s,%s)',(uid, a, n, d, 'student'))
                cur.execute('insert into students.users (id, student_number, condition) values (%s,%s,%s)', (uid,leg,''))
                cur.execute('insert into credentials.user_password (id, user_id, username, password) values (%s,%s,%s,%s)',(str(uuid.uuid4()), uid, d, d))
    finally:
        cur.close()
        con.commit()
finally:
    con.close()
