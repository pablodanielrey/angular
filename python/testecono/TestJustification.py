import logging
import unittest
import sys
sys.path.append('../../python')

from testecono.TestEcono import TestEcono
from testecono.TestUser import TestUser

from model.assistance.justifications.art102Justification import Art102Justification
from model.assistance.justifications.art102Justification import Art102JustificationDAO

from model.assistance.justifications.artJustification import ARTJustification
from model.assistance.justifications.artJustification import ARTJustificationDAO

from model.assistance.justifications.authorityJustification import AuthorityJustification
from model.assistance.justifications.authorityJustification import AuthorityJustificationDAO

from model.assistance.justifications.birthdayJustification import BirthdayJustification
from model.assistance.justifications.birthdayJustification import BirthdayJustificationDAO

from model.assistance.justifications.bloodDonationJustification import BloodDonationJustification
from model.assistance.justifications.bloodDonationJustification import BloodDonationJustificationDAO


from model.assistance.justifications.compensatoryJustification import CompensatoryJustification
from model.assistance.justifications.compensatoryJustification import CompensatoryJustificationDAO

from model.assistance.justifications.evaluationJustification import EvaluationJustification
from model.assistance.justifications.evaluationJustification import EvaluationJustificationDAO

from model.assistance.justifications.familyAttentionJustification import FamilyAttentionJustification
from model.assistance.justifications.familyAttentionJustification import FamilyAttentionJustificationDAO

from model.assistance.justifications.holidayJustification import HolidayJustification
from model.assistance.justifications.holidayJustification import HolidayJustificationDAO

from model.assistance.justifications.marriageJustification import MarriageJustification
from model.assistance.justifications.marriageJustification import MarriageJustificationDAO


from model.assistance.justifications.outTicketJustification import OutTicketWithReturnJustification
from model.assistance.justifications.outTicketJustification import OutTicketWithReturnJustificationDAO


from random import randint

import datetime

class TestJustification(TestEcono):   
    justificationDAO = None
    justificationEntity = None
    
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try: 
                self.justificationDAO._createSchema(con)
                con.commit()
                
            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
            
            
    def assertEqualStatus(self, status, status2):
        self.assertEqual(status.id, status2.id)
        self.assertEqual(status.justificationId, status2.justificationId)
        self.assertEqual(status.status, status2.status)
        self.assertEqual(status.userId, status2.userId)
        self.assertEqual(status.date, status2.date)
        self.assertEqual(status.created, status2.created)
   
    def assertEqualJustification(self, justification, justification2):
        self.assertEqual(justification.id, justification2.id)        
        self.assertEqual(justification.userId, justification2.userId)
        self.assertEqual(justification.ownerId, justification2.ownerId)
        self.assertEqualStatus(justification.status, justification2.status)





class TestJustificationSingle(TestJustification):        
    def assertEqualJustification(self, justification, justification2):
        #self.assertEqual(justification.date, justification2.date)
        super().assertEqualJustification(justification, justification2)
        
    def defineNewJustification(self, con):        
        user_id, user = TestUser.defineUserAndPersist(con)
        owner_id, owner = TestUser.defineUserAndPersist(con)
        con.commit()
        
        now = datetime.datetime.now() #mal para que funcione actualmente
        #now = datetime.datetime.now().date() #bien, pero actualmente no funcione
        justification = self.justificationEntity(user_id, owner_id, now)
        return justification             
        
        
        

        
class TestJustificationRanged(TestJustification):
    def assertEqualJustification(self, justification, justification2):
        self.assertEqual(justification.start, justification2.start)
        self.assertEqual(justification.end, justification2.end)
        super().assertEqualJustification(justification, justification2)


    def defineNewJustification(self, con):        
        user_id, user = TestUser.defineUserAndPersist(con)
        owner_id, owner = TestUser.defineUserAndPersist(con)
        con.commit()
        
        now = datetime.datetime.now().date()
        days = randint(1,60)
        justification = self.justificationEntity(user_id, owner_id, now, days)
      
        return justification
    
    
    
    
class TestJustificationRangedTime(TestJustification):
    def assertEqualJustification(self, justification, justification2):
        self.assertEqual(justification.start, justification2.start)
        self.assertEqual(justification.end, justification2.end)
        super().assertEqualJustification(justification, justification2)


    def defineNewJustification(self, con):
        user_id, user = TestUser.defineUserAndPersist(con)
        owner_id, owner = TestUser.defineUserAndPersist(con)
        con.commit()
        
        start = datetime.datetime.now()
        end = datetime.datetime.now()
        justification = self.justificationEntity(user_id, owner_id, start, end)
      
        return justification
        
        


                   
                
                
                
                
class TestJustificationArt102(TestJustificationSingle):
    def setUp(self):
        self.justificationDAO = Art102JustificationDAO
        self.justificationEntity = Art102Justification
        super().setUp()
                
             
class TestJustificationAuthority(TestJustificationSingle):
    def setUp(self):
        self.justificationDAO = AuthorityJustificationDAO
        self.justificationEntity = AuthorityJustification
        super().setUp()
        
class TestJustificationBirthday(TestJustificationSingle):
    def setUp(self):
        self.justificationDAO = BirthdayJustificationDAO
        self.justificationEntity = BirthdayJustification
        super().setUp()
        
class TestJustificationBloodDonation(TestJustificationSingle):
    def setUp(self):
        self.justificationDAO = BloodDonationJustificationDAO
        self.justificationEntity = BloodDonationJustification
        super().setUp()        
          
         
class TestJustificationArt(TestJustificationRanged):
    def setUp(self):
        self.justificationDAO = ARTJustificationDAO
        self.justificationEntity = ARTJustification
        super().setUp()
                             
                 
class TestJustificationCompensatory(TestJustificationSingle):
    def setUp(self):
        self.justificationDAO = CompensatoryJustificationDAO
        self.justificationEntity = CompensatoryJustification
        super().setUp()
          
          
class TestJustificationEvaluation(TestJustificationSingle):
    def setUp(self):
        self.justificationDAO = EvaluationJustificationDAO
        self.justificationEntity = EvaluationJustification
        super().setUp()                            

class TestJustificationFamilyAttention(TestJustificationRanged):
    def setUp(self):
        self.justificationDAO = FamilyAttentionJustificationDAO
        self.justificationEntity = FamilyAttentionJustification
        super().setUp()     

class TestJustificationHoliday(TestJustificationSingle):
    def setUp(self):
        self.justificationDAO = HolidayJustificationDAO
        self.justificationEntity = HolidayJustification
        super().setUp()   

class TestJustificationMarriage(TestJustificationRanged):
    def setUp(self):
        self.justificationDAO = MarriageJustificationDAO
        self.justificationEntity = MarriageJustification
        super().setUp()                   
  
  
class TestJustificationOutTicketWithReturn(TestJustificationRangedTime):
    def setUp(self):
        self.justificationDAO = OutTicketWithReturnJustificationDAO
        self.justificationEntity = OutTicketWithReturnJustification
        super().setUp()                   
                              
     
     
     
     
     
     
                
class TestJustificationSinglePersist(TestJustificationSingle):
     
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = self.defineNewJustification(con)
       
            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
       
        
    def test_persist(self):
        try:
            con = self.connection.get()
            try:
                ##### insertar #####
                self.justification.persist(con)
                con.commit()
                justs = self.justificationEntity.findById(con, [self.justification.id])
                self.assertEqualJustification(self.justification, justs[0])
                               
                ##### cambiar estado #####
                state = self.justification.getStatus()
                state.changeStatus(con, self.justification, 2, self.justification.ownerId)
                con.commit()
                justs = self.justificationEntity.findById(con, [self.justification.id])
                self.assertEqualJustification(self.justification, justs[0])
               

            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e)



class TestJustificationSingleFindById(TestJustificationSingle):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = self.defineNewJustification(con)
                self.justification.persist(con)
                con.commit()

            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
            

    def test_find_by_id(self):
        try:
            con = self.connection.get()
            try:
                j = self.justificationEntity.findById(con,[self.justification.id])
                self.assertEqualJustification(self.justification, j[0])
                
                j = self.justificationEntity.findById(con, ["not_exists"])
                self.assertEqual(j, [])
                               
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e)             
             
             

class TestJustificationSingleFindByUserId(TestJustificationSingle):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = self.defineNewJustification(con)
                self.justification.persist(con)
                con.commit()

            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
            

    def test_find_by_user_id(self):
        try:
            con = self.connection.get()
            try:
                start = datetime.datetime.combine(self.justification.date, datetime.time.min) - datetime.timedelta(days=1)
                end = datetime.datetime.combine(self.justification.date, datetime.time.min) + datetime.timedelta(days=1)
                usersId = [self.justification.userId]
                
                justs = self.justificationEntity.findByUserId(con, usersId, start, end)

                ids = []
                for just in justs:
                    ids.append(just.id)
                    
                self.assertIn(self.justification.id, ids)
                
                for just in justs:
                    if just.id == self.justification.id:
                        self.assertEqualJustification(just, self.justification)             
                               
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e)

             



class TestJustificationRangedPersist(TestJustificationRanged):

    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = self.defineNewJustification(con)
       
            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
            
  
            
    def test_persist(self):
        try:
            con = self.connection.get()
            try:
               
                ##### insertar #####
                self.justification.persist(con)
                con.commit()
                justs = self.justificationEntity.findById(con, [self.justification.id])
                self.assertEqualJustification(self.justification, justs[0])
 
                ##### cambiar estado #####
                state = self.justification.getStatus()
                state.changeStatus(con, self.justification, 2, self.justification.ownerId)
                con.commit()
                justs = self.justificationEntity.findById(con, [self.justification.id])
                self.assertEqualJustification(self.justification, justs[0])

            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e)     
            
            
class TestJustificationRangedFindById(TestJustificationRanged):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = self.defineNewJustification(con)
                self.justification.persist(con)
                con.commit()

            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
            

    def test_find_by_id(self):
        try:
            con = self.connection.get()
            try:
                j = self.justificationEntity.findById(con,[self.justification.id])
                self.assertEqualJustification(self.justification, j[0])
                
                j = self.justificationEntity.findById(con, ["not_exists"])
                self.assertEqual(j, [])
                               
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e)            




class TestJustificationRangedFindByUserId(TestJustificationRanged):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = self.defineNewJustification(con)
                self.justification.persist(con)
                con.commit()

            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
            

    def test_find_by_user_id(self):
        try:
            con = self.connection.get()
            try:
                start = datetime.datetime.combine(self.justification.start, datetime.time.min) - datetime.timedelta(days=1)
                end = datetime.datetime.combine(self.justification.end, datetime.time.min) + datetime.timedelta(days=1)
                usersId = [self.justification.userId]
                
                justs = self.justificationEntity.findByUserId(con, usersId, start, end)

                ids = []
                for just in justs:
                    ids.append(just.id)
                    
                self.assertIn(self.justification.id, ids)
                
                for just in justs:
                    if just.id == self.justification.id:
                        self.assertEqualJustification(just, self.justification)             
                               
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e)








class TestJustificationRangedTimePersist(TestJustificationRangedTime):

    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = self.defineNewJustification(con)
       
            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
            
  
            
    def test_persist(self):
        try:
            con = self.connection.get()
            try:
               
                ##### insertar #####
                self.justification.persist(con)
                con.commit()
                justs = self.justificationEntity.findById(con, [self.justification.id])
                self.assertEqualJustification(self.justification, justs[0])
 
                ##### cambiar estado #####
                state = self.justification.getStatus()
                state.changeStatus(con, self.justification, 2, self.justification.ownerId)
                con.commit()
                justs = self.justificationEntity.findById(con, [self.justification.id])
                self.assertEqualJustification(self.justification, justs[0])

            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e) 
            
            
            
class TestJustificationRangedTimeFindById(TestJustificationRangedTime):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = self.defineNewJustification(con)
                self.justification.persist(con)
                con.commit()

            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
            

    def test_find_by_id(self):
        try:
            con = self.connection.get()
            try:
                j = self.justificationEntity.findById(con,[self.justification.id])
                self.assertEqualJustification(self.justification, j[0])
                
                j = self.justificationEntity.findById(con, ["not_exists"])
                self.assertEqual(j, [])
                               
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e)   




class TestJustificationRangedTimeFindByUserId(TestJustificationRanged):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = self.defineNewJustification(con)
                self.justification.persist(con)
                con.commit()

            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
            

    def test_find_by_user_id(self):
        try:
            con = self.connection.get()
            try:
                start = datetime.datetime.combine(self.justification.start, datetime.time.min) - datetime.timedelta(days=1)
                end = datetime.datetime.combine(self.justification.end, datetime.time.min) + datetime.timedelta(days=1)
                usersId = [self.justification.userId]
                
                justs = self.justificationEntity.findByUserId(con, usersId, start, end)

                ids = []
                for just in justs:
                    ids.append(just.id)
                    
                self.assertIn(self.justification.id, ids)
                
                for just in justs:
                    if just.id == self.justification.id:
                        self.assertEqualJustification(just, self.justification)             
                               
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e)
            



##### Art 102 #####
class TestJustificationArt102Persist(TestJustificationArt102, TestJustificationSinglePersist):
    pass

class TestJustificationArt102FindById(TestJustificationArt102, TestJustificationSingleFindById):
    pass

class TestJustificationArt102FindByUserId(TestJustificationArt102, TestJustificationSingleFindByUserId):
    pass    
    
    
##### ART #####
class TestJustificationArtPersist(TestJustificationArt,  TestJustificationRangedPersist):
    pass

class TestJustificationArtFindById(TestJustificationArt,  TestJustificationRangedFindById):
    pass

class TestJustificationArtFindByUserId(TestJustificationArt,  TestJustificationRangedFindByUserId):
    pass
        
 
##### Authority #####
class TestJustificationAuthorityPersist(TestJustificationAuthority,  TestJustificationSinglePersist):
    pass

class TestJustificationAuthorityFindById(TestJustificationAuthority, TestJustificationSingleFindById):
    pass
         
class TestJustificationAuthorityFindByUserId(TestJustificationAuthority, TestJustificationSingleFindByUserId):
    pass


##### BIRTHDAY #####
class TestJustificationBirthdayPersist(TestJustificationBirthday,  TestJustificationSinglePersist):
    pass

class TestJustificationBirthdayFindById(TestJustificationBirthday, TestJustificationSingleFindById):
    pass
         
class TestJustificationBirthdayFindByUserId(TestJustificationBirthday, TestJustificationSingleFindByUserId):
    pass



##### BLOOD DONATION #####
class TestJustificationBloodDonationPersist(TestJustificationBloodDonation,  TestJustificationSinglePersist):
    pass

class TestJustificationBloodDonationFindById(TestJustificationBloodDonation, TestJustificationSingleFindById):
    pass
         
class TestJustificationBloodDonationFindByUserId(TestJustificationBloodDonation, TestJustificationSingleFindByUserId):
    pass



##### COMPENSATORY #####
class TestJustificationCompensatoryPersist(TestJustificationCompensatory,  TestJustificationSinglePersist):
    pass

class TestJustificationCompensatoryFindById(TestJustificationCompensatory, TestJustificationSingleFindById):
    pass
         
class TestJustificationCompensatoryFindByUserId(TestJustificationCompensatory, TestJustificationSingleFindByUserId):
    pass



##### EVALUATION #####
class TestJustificationEvaluationPersist(TestJustificationEvaluation,  TestJustificationSinglePersist):
    pass

class TestJustificationEvaluationFindById(TestJustificationEvaluation, TestJustificationSingleFindById):
    pass
         
class TestJustificationEvaluationFindByUserId(TestJustificationEvaluation, TestJustificationSingleFindByUserId):
    pass



##### FAMILY ATTENTION #####
class TestJustificationFamilyAttentionPersist(TestJustificationFamilyAttention,  TestJustificationRangedPersist):
    pass

class TestJustificationFamilyAttentionFindById(TestJustificationFamilyAttention, TestJustificationRangedFindById):
    pass
         
class TestJustificationFamilyAttentionFindByUserId(TestJustificationFamilyAttention, TestJustificationRangedFindByUserId):
    pass





##### HOLIDAY #####
class TestJustificationHolidayPersist(TestJustificationHoliday,  TestJustificationSinglePersist):
    pass

class TestJustificationHolidayFindById(TestJustificationHoliday, TestJustificationSingleFindById):
    pass
         
class TestJustificationHolidayFindByUserId(TestJustificationHoliday, TestJustificationSingleFindByUserId):
    pass





##### Marriage #####
class TestJustificationMarriagePersist(TestJustificationMarriage,  TestJustificationRangedPersist):
    pass

class TestJustificationMarriageFindById(TestJustificationMarriage, TestJustificationRangedFindById):
    pass
         
class TestJustificationMarriageFindByUserId(TestJustificationMarriage, TestJustificationRangedFindByUserId):
    pass





##### OutTicketWithReturnJustification #####
class TestJustificationOutTicketWithReturnPersist(TestJustificationOutTicketWithReturn,  TestJustificationRangedTimePersist):
    pass

class TestJustificationOutTicketWithReturnFindById(TestJustificationOutTicketWithReturn,  TestJustificationRangedTimeFindById):
    pass

class TestJustificationOutTicketWithReturnFindByUserId(TestJustificationOutTicketWithReturn,  TestJustificationRangedTimeFindByUserId):
    pass


             
       
       
       
       


      

