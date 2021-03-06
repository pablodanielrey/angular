#!/usr/bin/python3
# -*- coding: UTF-8 -*-#
import cgitb
import cgi; cgitb.enable()  # opcional para debug
import logging
import inject
import re
import codecs
import psycopg2
import sys
sys.path.insert(0, '../../python')

logging.basicConfig(level=logging.DEBUG)

#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

"""
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
"""

from model.systems.files.files import Files
from model.systems.laboralInsertion.laboralInsertion import LaboralInsertion
from model.config import Config

def config_injector(binder):
    binder.bind(Config, Config('server-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)

def _getDatabase(config):
    host = config.configs['database_host']
    dbname = config.configs['database_database']
    user = config.configs['database_user']
    passw = config.configs['database_password']
    return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

files = inject.instance(Files)
lb = inject.instance(LaboralInsertion)

con = _getDatabase(config)
try:
    url = 'http://163.10.17.15'
    lb.download(con, url, '../tmp/')

    print("Content-Type: text/html")
    print()
    print("<html><body>" +
        "<div>info actualizada</div>" +
        "<div><a href=\"{}/cv/\" target=\"_blank\">acceder</a></div>".format(url) +
        "</body></hmtl>")



    """
    f = files.findById(con, fid)
    if f is None:
        print("Status: 403 Forbidden\r\n\r\n")
        print("no permitido")
        sys.exit(1)


    mimetype = f['mimetype'] if ['mimetype'] != '' else 'application/binary'
    #edata = bytes(f['content'])

    #logging.debug(edata)

    import base64
    #data = base64.b64decode(edata)

    #logging.debug(data)

    print("Content-Type: {}\n".format(mimetype))
    #rint("Content-Length: {}".format(len(data)))
    #print()
    sys.stdout.flush()
    #sys.stdout.buffer.write(data)
    sys.stdout.buffer.write(base64.b64decode(f['content']))
    """

finally:
    con.close()
