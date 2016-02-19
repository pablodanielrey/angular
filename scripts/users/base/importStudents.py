# -*- coding: utf-8 -*-
'''
    Crea un alumno en la base de datos.
'''

import sys

if __name__ == '__main__':

    print(sys.path)

    import createStudent
    import csv
    reader = csv.reader(sys.stdin)
    for name, lastname, dni, sn in reader:
        print('\n\n{} {} {} {}'.format(name,lastname,dni,sn))
        createStudent.createStudent(dni, name, lastname, sn)
