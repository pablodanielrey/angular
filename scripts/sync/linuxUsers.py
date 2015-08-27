# -*- coding: utf-8 -*-
import inject
import logging
import psycopg2
import sys
import crypt

if __name__ == '__main__':

    if len(sys.argv) < 5:
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    dbpassword = sys.argv[4]
    db = sys.argv[5]
    con = psycopg2.connect(host=host, port=port, user=user, password=dbpassword, dbname=db)
    try:
        cur = con.cursor()
        cur.execute('select username,password from credentials.user_password up, domain.users du where up.user_id = du.id')
        if cur.rowcount <= 0:
            sys.exit()

        uid = 1000
        gid = 1000
        f = open('/tmp/passwd', 'w')
        f2 = open('/tmp/group', 'w')
        f3 = open('/tmp/shadow', 'w')
        try:
            for (username, password) in cur:
                f.write('{0}:x:{1}:{2}:{0}:/home/{0}:/bin/bash\n'.format(username, uid, gid))
                f2.write('{0}:x:{1}:{0}\n'.format(username, gid))
                f3.write('{0}:{1}:::::::\n'.format(username, crypt.crypt(password)))
                uid = uid + 1
                gid = gid + 1

        finally:
            f.close()
            f2.close()
            f3.close()

    finally:
        con.close()
