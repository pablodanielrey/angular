
import sys
import uuid
import psycopg2
import psycopg2.pool
from psycopg2.extras import DictCursor


h = sys.argv[1]
u1 = sys.argv[2]
p1 = sys.argv[3]
u2 = sys.argv[4]
p2 = sys.argv[5]


with open('/tmp/querys.sql', 'w') as q:

    pool2 = psycopg2.pool.ThreadedConnectionPool(1, 4, host=h, database='dcsys', user=u1, password=p1, cursor_factory=DictCursor)
    con2 = pool2.getconn()
    try:

        pool = psycopg2.pool.ThreadedConnectionPool(1, 4, host=h, database='au24', user=u2, password=p2, cursor_factory=DictCursor)
        con = pool.getconn()
        try:
            f = sys.argv[6]

            users = []
            withDni = []

            with open(f,'r') as fi, open('/tmp/salida.csv','w') as o:
                import csv
                cr = csv.reader(fi)
                for r in cr:
                    cur = con.cursor()
                    cur.execute('select 1 from mdl_user where username like %s', (r[4].lower(),))
                    if cur.rowcount <= 0:
                        users.append(r)
                    else:
                        withDni.append(r)
                        o.write(r[0] + ',' + r[4] + '\n')

            ''' agrego los usuarios que falten en el fce '''
            for u in users:
                cur = con2.cursor()
                cur.execute('select id from profile.users where dni = %s', (u[4],))
                uid = None
                if cur.rowcount <= 0:
                    print('agregando a fce {}'.fotmat(u))
                    uid = str(uuid.uuid4())

                    cur.execute('insert into profile.users (id, dni, name, lastname, ) values (%s, %s, %s, %s)',
                                (uid, u[4], u[2], u[3]))
                    q.write(cur.query.decode('utf8'))
                    q.write('\n')

                    cur.execute('insert into credentials.user_password (id, user_id, username, password) values (%s, %s, %s, %s)',
                                (str(uuid.uuid4()), uid, u[4], 'algo'))
                    q.write(cur.query.decode('utf8'))
                    q.write('\n')
                else:
                    uid = cur.fetchone()['id']

                email = u[1].strip().lower()
                if 'econo.unlp.edu.ar' in email:
                    cur.execute('select * from profile.mails where email ilike %s', (email,))
                    if cur.rowcount <= 0:
                        cur.execute('insert into profile.mails (id, user_id, email, confirmed) values (%s, %s, %s, %s)',
                                    (str(uuid.uuid4()), uid, email.lower(), True))
                        q.write(cur.query.decode('utf8'))
                        q.write('\n')
                else:
                    cur.execute('select 1 from profile.mails where user_id = %s and email ilike %s', (uid, '%econo.unlp.edu.ar'))
                    if cur.rowcount <= 0:
                        o.write('No tiene cuenta econo {} {} {}\n'.format(u[0], u[4], email))

            con2.commit()

            ''' actualizo el nombre de usuario a dni en el aula virtual '''
            for u in users:
                cur = con.cursor()
                cur.execute('update mdl_user set username = %s where username = %s', (u[4], u[0]))
                q.write(cur.query.decode('utf8'))
                q.write('\n')
            con.commit()

        finally:
            pool.putconn(con)
    finally:
        pool2.putconn(con2)
