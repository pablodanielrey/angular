# -*- coding: utf-8 -*-
'''
    Crea un alumno en la base de datos.
    forma de invocacón de ejemplo:

    cat /tmp/archivo.csv | PYTHONPATH="../../../python/model" python3 importUsers.py

'''

import sys
import inject
from connection.connection import Connection

if __name__ == '__main__':

    print(sys.path)

    inject.configure()
    conn = inject.instance(Connection)
    con = conn.get()
    try:
        import createUser
        import csv
        reader = csv.reader(sys.stdin)
        for name, lastname, dni in reader:
            print('\n\n{} {} {}'.format(name,lastname,dni))
            createUser.createUser(con, dni, name, lastname)

        con.commit()

    finally:
        conn.put(con)
