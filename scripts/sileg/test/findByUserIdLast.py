# -*- coding: utf-8 -*-
import sys
sys.path.append('../../../python')

import inject
inject.configure()

import logging
logging.getLogger().setLevel(logging.INFO)


from model.registry import Registry
from model.connection import connection
from model.sileg.place.place import Place
from model.sileg.position.position import Position
from model.sileg.designation.designation import Designation
from model.sileg.designation.designation import OriginalDesignation
from model.sileg.designation.designation import Extension
from model.sileg.designation.designation import Prorogation
from model.sileg.designation.designation import ProrogationOriginal
from model.sileg.designation.designation import ProrogationExtension
from model.sileg.licence.licence import Licence
from model.users.users import User



if __name__ == '__main__':

    import logging
    reg = inject.instance(Registry)

    dcsysConn = connection.Connection(reg.getRegistry('dcsys2'))

    conD = dcsysConn.get()
    try:
        designations = Designation.findLasts(conD)
        print(designations)
        


    finally:
        dcsysConn.put(conD)

