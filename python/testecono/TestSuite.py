# -*- coding: utf-8 -*-
import unittest

import sys
sys.path.append('../../python')


from testecono.TestUser import TestUserPersist
from testecono.TestUser import TestUserDelete
from testecono.TestUser import TestUserFindById
from testecono.TestUser import TestUserFindAll


from testecono.TestJustification import *



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
    test_suite.addTest(TestJustificationArt102('test_persist'))
    test_suite.addTest(TestJustificationArt102('test_find_by_id'))
    test_suite.addTest(TestJustificationArt102('test_find_by_user_id'))
    
    ##### ART #####
    test_suite.addTest(TestJustificationArt('test_persist'))
    test_suite.addTest(TestJustificationArt('test_find_by_id'))
    test_suite.addTest(TestJustificationArt('test_find_by_user_id'))    

    ##### AUTHORITY #####
    test_suite.addTest(TestJustificationAuthority('test_persist'))
    test_suite.addTest(TestJustificationAuthority('test_find_by_id'))
    test_suite.addTest(TestJustificationAuthority('test_find_by_user_id'))        
    
    ##### AUTHORITY #####
    test_suite.addTest(TestJustificationBirthday('test_persist'))
    test_suite.addTest(TestJustificationBirthday('test_find_by_id'))
    test_suite.addTest(TestJustificationBirthday('test_find_by_user_id'))     
    
    ##### BLOOD DONATION #####
    test_suite.addTest(TestJustificationBloodDonation('test_persist'))
    test_suite.addTest(TestJustificationBloodDonation('test_find_by_id'))
    test_suite.addTest(TestJustificationBloodDonation('test_find_by_user_id'))    
    
    ##### COMPENSATORY #####
    test_suite.addTest(TestJustificationCompensatory('test_persist'))  
    test_suite.addTest(TestJustificationCompensatory('test_find_by_id'))
    test_suite.addTest(TestJustificationCompensatory('test_find_by_user_id'))    
     
    ##### EVALUATION #####
    test_suite.addTest(TestJustificationEvaluation('test_persist'))  
    test_suite.addTest(TestJustificationEvaluation('test_find_by_id'))
    test_suite.addTest(TestJustificationEvaluation('test_find_by_user_id'))    
    
    ##### FAMILY ATTENTION #####
    test_suite.addTest(TestJustificationFamilyAttention('test_persist'))  
    test_suite.addTest(TestJustificationFamilyAttention('test_find_by_id'))
    test_suite.addTest(TestJustificationFamilyAttention('test_find_by_user_id'))    
        
    ##### HOLIDAY #####
    test_suite.addTest(TestJustificationHoliday('test_persist'))  
    test_suite.addTest(TestJustificationHoliday('test_find_by_id'))
    test_suite.addTest(TestJustificationHoliday('test_find_by_user_id'))            
           
    ##### INFORMED ABSENCE #####
    test_suite.addTest(TestJustificationInformedAbsence('test_persist'))  
    test_suite.addTest(TestJustificationInformedAbsence('test_find_by_id'))
    test_suite.addTest(TestJustificationInformedAbsence('test_find_by_user_id'))   
    
    
    ##### LATE ARRIVAL #####
    test_suite.addTest(TestJustificationLateArrival('test_persist'))  
    test_suite.addTest(TestJustificationLateArrival('test_find_by_id'))
    test_suite.addTest(TestJustificationLateArrival('test_find_by_user_id'))   
    
    ##### LEAVE WITHOUT SALARY #####
    test_suite.addTest(TestJustificationLeaveWithoutSalary('test_persist'))  
    test_suite.addTest(TestJustificationLeaveWithoutSalary('test_find_by_id'))
    test_suite.addTest(TestJustificationLeaveWithoutSalary('test_find_by_user_id'))  
    
    ##### LIBRARIAN DAY #####
    test_suite.addTest(TestJustificationLibrarianDay('test_persist'))  
    test_suite.addTest(TestJustificationLibrarianDay('test_find_by_id'))
    test_suite.addTest(TestJustificationLibrarianDay('test_find_by_user_id'))  
    
    
    ##### LONG DURATION #####
    test_suite.addTest(TestJustificationLongDuration('test_persist'))  
    test_suite.addTest(TestJustificationLongDuration('test_find_by_id'))
    test_suite.addTest(TestJustificationLongDuration('test_find_by_user_id'))  
    
    ##### MARRIAGE #####
    test_suite.addTest(TestJustificationMarriage('test_persist'))  
    test_suite.addTest(TestJustificationMarriage('test_find_by_id'))
    test_suite.addTest(TestJustificationMarriage('test_find_by_user_id'))        

    ##### MATERNITY #####
    test_suite.addTest(TestJustificationMaternity('test_persist'))  
    test_suite.addTest(TestJustificationMaternity('test_find_by_id'))
    test_suite.addTest(TestJustificationMaternity('test_find_by_user_id'))
    
    ##### MEDICAL BOARD #####
    test_suite.addTest(TestJustificationMedicalBoard('test_persist'))  
    test_suite.addTest(TestJustificationMedicalBoard('test_find_by_id'))
    test_suite.addTest(TestJustificationMedicalBoard('test_find_by_user_id')) 
        
    
    ##### OUT TICKET #####
    test_suite.addTest(TestJustificationOutTicketWithReturn('test_persist'))  
    test_suite.addTest(TestJustificationOutTicketWithReturn('test_find_by_id'))
    test_suite.addTest(TestJustificationOutTicketWithReturn('test_find_by_user_id'))    
                   
    return test_suite
    
mySuit=suite()
  


runner=unittest.TextTestRunner()
runner.run(mySuit)

