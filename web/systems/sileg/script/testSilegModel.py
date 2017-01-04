# -*- coding: utf-8 -*-
import sys
sys.path.append('/root/issues/python') #definir ruta de acceso al modelo

import datetime
import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection import connection
from model.sileg.sileg import SilegModel
from model.designation.designation import DesignationDAO


if __name__ == '__main__':

    reg = inject.instance(Registry)
    conn = connection.Connection(reg.getRegistry('crossbar'))
    con = conn.get()


    try:

        print(DesignationDAO.findByFields(con,
          {
            #"dstart":[datetime.date(2016, 12, 16)],
            "office_id":["9365e0de-baec-4216-9b32-199f23707369"],
            "dout":"NULL",
            "description":"NOT NULL"
          }
        ))



        """
        users = SilegModel.getUsers(con)
        for user in users:
            positions = SilegModel.findPositionsActiveByUser(con, user.id)
            #print(positions)


        places = SilegModel.getCathedras(con)
        for place in places:
            positions = SilegModel.findPositionsActiveByPlace(con, place.id)
        """


    finally:
        conn.put(con)
