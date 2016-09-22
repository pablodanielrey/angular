# -*- coding: utf-8 -*-
import psycopg2
import sys, logging, subprocess


host = sys.argv[1]
port = sys.argv[2]
user = sys.argv[3]
passw = sys.argv[4]
db = sys.argv[5]
username = sys.argv[6]

con = psycopg2.connect(host=host, port=port, user=user, password=passw, dbname=db)
try:
    cur = con.cursor()
    cur.execute('select password from credentials.user_password where username = %s',(username,))
    cur.rowcount <= 0:
        logging.severe('no existe ningún usuario : {}'.format(username))
        sys.exit(1)

    pp = cur.fetchone()
    passww = pp['password']

    subprocess.call(['passwd',passww], shell=False)

except Exception as e:
    logging.exception(e)

finally:
    con.close()
