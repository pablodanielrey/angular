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
        cur.execute('select username from credentials.user_password up, domain.users du where up.user_id = du.id')
        if cur.rowcount <= 0:
            sys.exit()

        existent = []
        for username in cur:
            existent.append(username[0])


        linesp = []
        f = open('/etc/passwd','r')
        try:
            for l in f:
                u = l.split(':')[0]
                if u not in existent:
                    linesp.append(l)

        finally:
            f.close()

        linesg = []
        f2 = open('/etc/group', 'r')
        try:
            for l in f2:
                u = l.split(':')[0]
                if u not in existent:
                    linesg.append(l)

        finally:
            f2.close()

        liness = []
        f3 = open('/etc/shadow', 'r')
        try:
            for l in f3:
                u = l.split(':')[0]
                if u not in existent:
                    liness.append(l)

        finally:
            f3.close()

        cur.execute('select username,password from credentials.user_password up, domain.users du where up.user_id = du.id')
        if cur.rowcount <= 0:
            sys.exit()


        uid = 1000
        gid = 1000
        f = open('/etc/passwd', 'w')
        f2 = open('/etc/group', 'w')
        f3 = open('/etc/shadow', 'w')
        try:
            for l in linesp:
                f.write(l)

            for l in linesg:
                f2.write(l)

            for l in liness:
                f3.write(l)

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
