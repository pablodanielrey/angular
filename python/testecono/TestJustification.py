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

    def assertEqualJustification(self, justification, justification2):
        self.assertEqual(justification.id, justification2.id)        
        self.assertEqual(justification.userId, justification2.userId)
        self.assertEqual(justification.ownerId, justification2.ownerId)        


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
                
                """
                uid = User.findByDni(con, self.user.dni)
                u = User.findById(con, [uid[0]])
                self.assertEqualUsers(self.user, u[0])                
                
                ##### actualizar #####
                self.user.name = "Test Nomb"
                self.user.persist(con)
                con.commit()
                uid = User.findByDni(con, self.user.dni)
                u = User.findById(con, [uid[0]])
                self.assertEqualUsers(self.user, u[0])
                
                ##### error #####
                user = self.defineUser()
                with self.assertRaises(Exception):
                    UserDAO.persist(con, user)
                """
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.error(str(e))        

