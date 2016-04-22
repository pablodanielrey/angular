import unittest

import sys
sys.path.append('../../python')

from testecono.TestUser import TestUserPersist
from testecono.TestUser import TestUserFindById



def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestUserPersist('test_persist_user'))
    test_suite.addTest(TestUserFindById('test_find_by_id'))
    return test_suite

mySuit=suite()


runner=unittest.TextTestRunner()
runner.run(mySuit)

