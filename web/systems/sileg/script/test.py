# -*- coding: utf-8 -*-
import sys
sys.path.append('/root/issues/python') #definir ruta de acceso al modelo


import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection import connection
from model.sileg.place.place import Place



if __name__ == '__main__':



    reg = inject.instance(Registry)
    silegConn = connection.Connection(reg.getRegistry('sileg'))
    con = silegConn.get()
    try:
        places = Place.findAll(con)
        print(places)

    finally:
        silegConn.put(con)
