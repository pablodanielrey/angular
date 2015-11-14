#!/usr/bin/python3
# -*- coding: UTF-8 -*-#
import cgitb
import cgi; cgitb.enable()  # opcional para debug
import logging
import inject
import re
import psycopg2
import codecs
import sys
sys.path.insert(0, '../../python')

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

logging.basicConfig(level=logging.DEBUG)

args = cgi.FieldStorage()
if "i" not in args:
    print("Status: 403 Forbidden\r\n\r\n")
    print("no argumentos")
    sys.exit(1)

fid = args.getvalue("i")
#if not re.search('/([a-zA-Z]+\-*)+/', fid):
#    print("Status: 403 Forbidden\r\n\r\n")
#    print("no valor {}".format(fid))
#    sys.exit(1)

from model.systems.files.files import Files
from model.config import Config


config = Config('server-config.cfg')

def _getDatabase(config):
    host = config.configs['database_host']
    dbname = config.configs['database_database']
    user = config.configs['database_user']
    passw = config.configs['database_password']
    return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

con = _getDatabase(config)
try:

    if fid == 'e':

        print("Content-Type: {}; charset=utf-8".format('text/csv'))
        print("Content-Disposition: attachment; filename=\"ingeso-errores.csv\"")
        print()

        cur = con.cursor()
        cur.execute('select error, names, dni, email, comment, created from ingreso.errors')
        for c in cur:
            errors = ''
            for a in c:
                errors = errors + str(a).replace("\"", '').replace(';', ',') + ';'
            print(errors)

    elif fid == 'p':

        print("Content-Type: {}; charset=utf-8".format('text/csv'))
        print("Content-Disposition: attachment; filename=\"ingeso.csv\"")
        print()

        cur = con.cursor()
        cur.execute('select name, lastname, dni, email from profile.users u left join profile.mails m on (u.id = m.user_id and m.confirmed) where u.id in (select id from students.users)')
        for c in cur:
            errors = ''
            for a in c:
                errors = errors + (a.replace("\"", '').replace(';', ',') if a is not None else ' ') + ';'
            print(errors)

    else:
        print("Status: 403 Forbidden\r\n\r\n")
        print()

finally:
    con.close()
