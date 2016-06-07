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


from model.connection.connection import Connection
from model.files.files import FileDAO
from model.registry import Registry

inject.configure()
r = inject.instance(Registry)
conn = Connection(r.getRegistry('dcsys'))

con = conn.get()
try:
    f = FileDAO.findById(con, fid)
    if f is None:
        print("Status: 403 Forbidden\r\n\r\n")
        print("no permitido")
        sys.exit(1)

    mimetype = f.mimetype if f.mimetype != '' else 'application/binary'
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
    content = FileDAO.getContent(con, f.id)
    sys.stdout.buffer.write(base64.b64decode(content))


finally:
    conn.put(con)
