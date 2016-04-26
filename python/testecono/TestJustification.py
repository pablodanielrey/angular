import logging
import unittest
import sys
sys.path.append('../../python')

from testecono.TestEcono import TestEcono
from testecono.TestUser import TestUser
from model.assistance.justifications.art102Justification import Art102Justification
from model.assistance.justifications.art102Justification import Art102JustificationDAO

import datetime

class TestJustification(TestEcono):
    
    def setUp(self):
        super(TestJustification, self).setUp()
        
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
        self.assertEqual(justification.ownerId, justification2.ownerId)
        self.assertEqualStatus(justification.status, justification2.status)

class TestJustificationArt102(TestJustification):
    
    def setUp(self):
        super(TestJustificationArt102, self).setUp()
        try:
            con = self.connection.get()
            try:
                Art102JustificationDAO._createSchema(con)
                con.commit()
       
            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.error(str(e))
        


                
                
                
                
class TestJustificationArt102Persist(TestJustificationArt102):
    def setUp(self):
        super(TestJustificationArt102Persist, self).setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = TestJustificationArt102Persist.defineNewJustification(con)

       
            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.error(str(e))
    
        
    @classmethod
    def defineNewJustification(cls, con):        
        user_id, user = TestUser.defineUserAndPersist(con)
        owner_id, owner = TestUser.defineUserAndPersist(con)
        con.commit()
        
        now = datetime.datetime.now()
        justification = Art102Justification(user_id, owner_id, now)
      
        return justification
            
            
            
    def test_persist(self):
        try:
            con = self.connection.get()
            try:
                ##### insertar #####
                self.justification.persist(con)
                con.commit()
                justs = Art102Justification.findById(con, [self.justification.id])
                self.assertEqualJustification(self.justification, justs[0])
                               
                ##### cambiar estado #####
                state = self.justification.getStatus()
                state.changeStatus(con, self.justification, 2, self.justification.ownerId)
                con.commit()
                justs = Art102Justification.findById(con, [self.justification.id])
                self.assertEqualJustification(self.justification, justs[0])
               

            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.error(str(e))        

