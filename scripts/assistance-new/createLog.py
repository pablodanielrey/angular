
import sys
import uuid
import psycopg2
import psycopg2.pool
from psycopg2.extras import DictCursor

h = sys.argv[1]
u1 = sys.argv[2]
p1 = sys.argv[3]

dni = sys.argv[4]
fech = sys.argv[5]

pool2 = psycopg2.pool.ThreadedConnectionPool(1, 4, host=h, database='dcsys', user=u1, password=p1, cursor_factory=DictCursor)
con = pool2.getconn()
try:

    cur = con.cursor()
    cur.execute('select id from profile.users where dni = %s', (dni,))
    uid = cur.fetchone()['id']

    cur.execute('select device_id from assistance.attlog where user_id = %s limit 1', (uid,))
    did = cur.fetchone()['device_id']

    cur.execute('insert into assistance.attlog (id, user_id, device_id, log, verifymode) values (%s, %s, %s, %s, %s)',
                (str(uuid.uuid4()), uid, did, fech, 0),)
    print(cur.query.decode('utf8'))
    con.commit()

finally:
    pool2.putconn(con)
