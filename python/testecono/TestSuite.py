import unittest

import sys
sys.path.append('../../python')

from testecono.TestUser import TestUserPersist



def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestUserPersist('test_persist_user'))
    return test_suite

mySuit=suite()


runner=unittest.TextTestRunner()
runner.run(mySuit)

