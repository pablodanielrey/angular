# -*- coding: utf-8 -*-
import sys
sys.path.append('/root/issues/python') #definir ruta de acceso al modelo
import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection import connection
from model.designation.designation import DesignationDAO

if __name__ == '__main__':
    reg = inject.instance(Registry)
    conn = connection.Connection(reg.getRegistry('sileg'))
    con = conn.get()

    try:
        print("crear esquema")
        DesignationDAO._createSchema(con)

    except Error:
        print("ERROR")
        print(Error)

    finally:
        conn.put(con)
