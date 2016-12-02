# -*- coding: utf-8 -*-
import sys
sys.path.append('/root/issues/python') #definir ruta de acceso al modelo

import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection import connection
from model.offices.office import OfficeModel
from model.offices.office import Office



if __name__ == '__main__':

    reg = inject.instance(Registry)
    conn = connection.Connection(reg.getRegistry('sileg'))
    con = conn.get()
    try:

        offices = Office.findAll(con)
        for o in offices:
            print(o)

        """

        places = SilegModel.getCathedras(con)
        for place in places:
            positions = SilegModel.findPositionsActiveByPlace(con, place.id)

        """

    finally:
        conn.put(con)
