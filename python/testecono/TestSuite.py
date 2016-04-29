import unittest

import sys
sys.path.append('../../python')


from testecono.TestUser import TestUserPersist
from testecono.TestUser import TestUserDelete
from testecono.TestUser import TestUserFindById
from testecono.TestUser import TestUserFindAll


##### ART 102 #####
from testecono.TestJustification import TestJustificationArt102Persist
from testecono.TestJustification import TestJustificationArt102FindById
from testecono.TestJustification import TestJustificationArt102FindByUserId

##### ART #####
from testecono.TestJustification import TestJustificationArtPersist
from testecono.TestJustification import TestJustificationArtFindById
from testecono.TestJustification import TestJustificationArtFindByUserId

##### AUTHORITY #####
from testecono.TestJustification import TestJustificationAuthorityPersist
from testecono.TestJustification import TestJustificationAuthorityFindById
from testecono.TestJustification import TestJustificationAuthorityFindByUserId

##### BIRTHDAY #####
from testecono.TestJustification import TestJustificationBirthdayPersist
from testecono.TestJustification import TestJustificationBirthdayFindById
from testecono.TestJustification import TestJustificationBirthdayFindByUserId

##### BLOOD DONATION #####
from testecono.TestJustification import TestJustificationBloodDonationPersist
from testecono.TestJustification import TestJustificationBloodDonationFindById
from testecono.TestJustification import TestJustificationBloodDonationFindByUserId

##### COMPENSATORY #####
from testecono.TestJustification import TestJustificationCompensatoryPersist
from testecono.TestJustification import TestJustificationCompensatoryFindById
from testecono.TestJustification import TestJustificationCompensatoryFindByUserId

##### EVALUATION #####
from testecono.TestJustification import TestJustificationEvaluationPersist
from testecono.TestJustification import TestJustificationEvaluationFindById
from testecono.TestJustification import TestJustificationEvaluationFindByUserId

##### FAMILY ATTENTION #####
from testecono.TestJustification import TestJustificationFamilyAttentionPersist
from testecono.TestJustification import TestJustificationFamilyAttentionFindById
from testecono.TestJustification import TestJustificationFamilyAttentionFindByUserId

##### HOLIDAY #####
from testecono.TestJustification import TestJustificationHolidayPersist
from testecono.TestJustification import TestJustificationHolidayFindById
from testecono.TestJustification import TestJustificationHolidayFindByUserId

##### MARRIAGE #####
from testecono.TestJustification import TestJustificationMarriagePersist
from testecono.TestJustification import TestJustificationMarriageFindById
from testecono.TestJustification import TestJustificationMarriageFindByUserId

##### OUT TICKET #####
from testecono.TestJustification import TestJustificationOutTicketWithReturnPersist
from testecono.TestJustification import TestJustificationOutTicketWithReturnFindById
from testecono.TestJustification import TestJustificationOutTicketWithReturnFindByUserId


def suite():
    """
        Gather all the tests from this module in a test suite.
    """        
    test_suite = unittest.TestSuite()


    test_suite.addTest(TestUserPersist('test_persist'))
    test_suite.addTest(TestUserDelete('test_delete'))
    test_suite.addTest(TestUserFindById('test_find_by_id'))
    test_suite.addTest(TestUserFindAll('test_find_all'))

    
    ##### ART 102 #####
    test_suite.addTest(TestJustificationArt102Persist('test_persist'))
    test_suite.addTest(TestJustificationArt102FindById('test_find_by_id'))   
    test_suite.addTest(TestJustificationArt102FindByUserId('test_find_by_user_id'))
    
    ##### ART #####
    test_suite.addTest(TestJustificationArtPersist('test_persist'))
    test_suite.addTest(TestJustificationArtFindById('test_find_by_id'))    
    test_suite.addTest(TestJustificationArtFindByUserId('test_find_by_user_id'))
        
    ##### AUTHORITY #####
    test_suite.addTest(TestJustificationAuthorityPersist('test_persist'))
    test_suite.addTest(TestJustificationAuthorityFindById('test_find_by_id'))   
    test_suite.addTest(TestJustificationAuthorityFindByUserId('test_find_by_user_id'))

    ##### BIRTHDAY #####
    test_suite.addTest(TestJustificationBirthdayPersist('test_persist'))
    test_suite.addTest(TestJustificationBirthdayFindById('test_find_by_id'))   
    test_suite.addTest(TestJustificationBirthdayFindByUserId('test_find_by_user_id'))

    ##### BLOOD DONATION #####
    test_suite.addTest(TestJustificationBloodDonationPersist('test_persist'))
    test_suite.addTest(TestJustificationBloodDonationFindById('test_find_by_id'))   
    test_suite.addTest(TestJustificationBloodDonationFindByUserId('test_find_by_user_id'))

    ##### BLOOD DONATION #####
    test_suite.addTest(TestJustificationCompensatoryPersist('test_persist'))
    test_suite.addTest(TestJustificationCompensatoryFindById('test_find_by_id'))   
    test_suite.addTest(TestJustificationCompensatoryFindByUserId('test_find_by_user_id'))
    
    ##### EVALUATION #####
    test_suite.addTest(TestJustificationEvaluationPersist('test_persist'))
    test_suite.addTest(TestJustificationEvaluationFindById('test_find_by_id'))   
    test_suite.addTest(TestJustificationEvaluationFindByUserId('test_find_by_user_id'))
    
    ##### FAMILY ATTENTION #####
    test_suite.addTest(TestJustificationFamilyAttentionPersist('test_persist'))
    test_suite.addTest(TestJustificationFamilyAttentionFindById('test_find_by_id'))   
    test_suite.addTest(TestJustificationFamilyAttentionFindByUserId('test_find_by_user_id'))
    
    ##### HOLIDAY #####
    test_suite.addTest(TestJustificationHolidayPersist('test_persist'))
    test_suite.addTest(TestJustificationHolidayFindById('test_find_by_id'))   
    test_suite.addTest(TestJustificationHolidayFindByUserId('test_find_by_user_id'))
    
    ##### MARRIAGE #####
    test_suite.addTest(TestJustificationMarriagePersist('test_persist'))
    test_suite.addTest(TestJustificationMarriageFindById('test_find_by_id'))   
    test_suite.addTest(TestJustificationMarriageFindByUserId('test_find_by_user_id'))    

    
    ##### OUT TICKET #####
    test_suite.addTest(TestJustificationOutTicketWithReturnPersist('test_persist'))
    test_suite.addTest(TestJustificationOutTicketWithReturnFindById('test_find_by_id'))   
    test_suite.addTest(TestJustificationOutTicketWithReturnFindByUserId('test_find_by_user_id'))   
     
    return test_suite
    
mySuit=suite()


runner=unittest.TextTestRunner()
runner.run(mySuit)

