import unittest

import sys
sys.path.append('../../python')

from testecono.TestUser import TestUserPersist
from testecono.TestUser import TestUserDelete
from testecono.TestUser import TestUserFindById
from testecono.TestUser import TestUserFindAll


from testecono.TestJustification import TestJustificationArt102Persist
from testecono.TestJustification import TestJustificationArt102FindById
from testecono.TestJustification import TestJustificationArt102FindByUserId

from testecono.TestJustification import TestJustificationArtPersist
from testecono.TestJustification import TestJustificationArtFindById
from testecono.TestJustification import TestJustificationArtFindByUserId

def suite():
    """
        Gather all the tests from this module in a test suite.
    """        
    test_suite = unittest.TestSuite()

    ###user###
    test_suite.addTest(TestUserPersist('test_persist'))
    test_suite.addTest(TestUserDelete('test_delete'))
    test_suite.addTest(TestUserFindById('test_find_by_id'))
    test_suite.addTest(TestUserFindAll('test_find_all'))

    ###single justification###
    test_suite.addTest(TestJustificationArt102Persist('test_persist'))
    test_suite.addTest(TestJustificationArt102FindById('test_find_by_id'))    
    test_suite.addTest(TestJustificationArt102FindByUserId('test_find_by_user_id'))

    ###ranged justification###
    test_suite.addTest(TestJustificationArtPersist('test_persist'))
    test_suite.addTest(TestJustificationArtFindById('test_find_by_id'))    
    test_suite.addTest(TestJustificationArtFindByUserId('test_find_by_user_id'))

    return test_suite
    
mySuit=suite()


runner=unittest.TextTestRunner()
runner.run(mySuit)

