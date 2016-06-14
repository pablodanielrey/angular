# -*- coding: utf-8 -*-
import unittest
import inject
inject.configure()

import sys
sys.path.append('../../../python')

from model.registry import Registry
from model.connection.connection import Connection

from model.sileg.silegdao import SilegDAO
from model.sileg.position.position import PositionDAO
from model.sileg.place.place import PlaceDAO
from model.sileg.designation.designation import DesignationDAO
from model.sileg.licence.licence import LicenceDAO

class TestSileg(unittest.TestCase):


    def test_create_database(self):

        reg = inject.instance(Registry)

        registrySection = reg.getRegistry('dcsys2')

        conn = Connection(registrySection)

        con = conn.get()
        try:
            SilegDAO._createSchema(con)
            con.commit()

        finally:
            conn.put(con)
