# -*- coding: utf-8 -*-
'''
    Crea un alumno en la base de datos.

    cat /tmp/archivo.csv | PYTHONPATH="../../../python/model" python3 importStudents.py
'''

from model.connection import connection
from model.registry import Registry
import sys

if __name__ == '__main__':

    import inject
    #inject.configure()
    r = inject.instance(Registry)
    conn = connection.Connection(r.getRegistry('dcsys'))
    con = conn.get()
    try:
        import createStudent
        import csv
        reader = csv.reader(sys.stdin)
        for name, lastname, dni, sn in reader:
            print('\n\n{} {} {} {}'.format(name,lastname,dni,sn))
            createStudent.createStudent(con, dni, name, lastname, sn)

        con.commit()

    finally:
        conn.put(con)
