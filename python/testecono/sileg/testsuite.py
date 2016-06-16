# -*- coding: utf-8 -*-
import unittest

import sys
sys.path.append('../../../python')


from testecono.sileg.testsileg import TestSileg



def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()

    test_suite.addTest(TestSileg('test_create_database'))

    return test_suite

mySuit=suite()


runner=unittest.TextTestRunner()
runner.run(mySuit)
