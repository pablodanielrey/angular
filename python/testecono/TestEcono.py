import unittest
import inject
inject.configure()

import sys
sys.path.append('../../python')


from model.registry import Registry
from model.connection.connection import Connection

class TestEcono(unittest.TestCase):

    def setUp(self):

        reg = inject.instance(Registry)
          
        registrySection = reg.getRegistry('dcsys2')

        self.connection = Connection(registrySection)
