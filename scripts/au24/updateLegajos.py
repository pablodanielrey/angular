
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
            users = {}
            cur = con.cursor()
            cur.execute('select username, idnumber from mdl_user')
            for c in cur:
                users[c['username']] = c['idnumber']

            usersFce = {}
            cur = con2.cursor()
            cur.execute('select dni, student_number from users_moodle where dni in %s', (tuple(users.keys()),))
            for c in cur:
                usersFce[c['dni']] = c['student_number']

            cur2 = con.cursor()
            for u in usersFce.keys():
                if usersFce[u] and usersFce[u] != users[u]:
                    cur2.execute('update mdl_user set idnumber = %s where username = %s', (usersFce[u], u))
                    query = cur2.query.decode('utf8')
                    q.write(query + '\n')
                    print(query)
                    con.commit()
                else:
                    q.write('{} tiene sincronizado el legajo {}\n'.format(u,usersFce[u]))

        finally:
            pool.putconn(con)
    finally:
        pool2.putconn(con2)
