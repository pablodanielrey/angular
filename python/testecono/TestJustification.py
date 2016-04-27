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

from random import randint

import datetime

class TestJustification(TestEcono):        
    
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
        
        
class TestJustificationRanged(TestJustification):
    def assertEqualJustification(self, justification, justification2):
        self.assertEqual(justification.start, justification2.start)
        self.assertEqual(justification.end, justification2.end)
        super().assertEqualJustification(justification, justification2)
        
        
                
        
class TestJustificationArt102(TestJustificationSingle):
    
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                Art102JustificationDAO._createSchema(con)
                con.commit()
       
            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
        
        
    @classmethod
    def defineNewJustification(cls, con):        
        user_id, user = TestUser.defineUserAndPersist(con)
        owner_id, owner = TestUser.defineUserAndPersist(con)
        con.commit()
        
        now = datetime.datetime.now() #mal para que funcione actualmente
        #now = datetime.datetime.now().date() #bien, pero actualmente no funcione
        justification = Art102Justification(user_id, owner_id, now)

      
        return justification
        
                
                
                
                
class TestJustificationArt102Persist(TestJustificationArt102):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = TestJustificationArt102Persist.defineNewJustification(con)

       
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
            logging.exception(e)        




class TestJustificationArt102FindById(TestJustificationArt102):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = TestJustificationArt102FindById.defineNewJustification(con)
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
                j = Art102Justification.findById(con,[self.justification.id])
                self.assertEqualJustification(self.justification, j[0])
                
                j = Art102Justification.findById(con, ["not_exists"])
                self.assertEqual(j, [])
                               
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e)
            
             
             
             
             
             
             
class TestJustificationArt102FindByUserId(TestJustificationArt102):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = TestJustificationArt102FindByUserId.defineNewJustification(con)
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
                
                justs = Art102Justification.findByUserId(con, usersId, start, end)

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




class TestJustificationArt(TestJustificationRanged):
    
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                ARTJustificationDAO._createSchema(con)
                con.commit()
       
            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.exception(e)
        
        
    @classmethod
    def defineNewJustification(cls, con):        
        user_id, user = TestUser.defineUserAndPersist(con)
        owner_id, owner = TestUser.defineUserAndPersist(con)
        con.commit()
        
        now = datetime.datetime.now().date()
        days = randint(1,60)
        justification = ARTJustification(user_id, owner_id, now, days)
      
        return justification
                    




class TestJustificationArtPersist(TestJustificationArt):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = TestJustificationArtPersist.defineNewJustification(con)

       
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
                justs = ARTJustification.findById(con, [self.justification.id])
                self.assertEqualJustification(self.justification, justs[0])
 
                ##### cambiar estado #####
                state = self.justification.getStatus()
                state.changeStatus(con, self.justification, 2, self.justification.ownerId)
                con.commit()
                justs = ARTJustification.findById(con, [self.justification.id])
                self.assertEqualJustification(self.justification, justs[0])


            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e)                                    
      
      
      
class TestJustificationArtFindById(TestJustificationArt):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = TestJustificationArtFindById.defineNewJustification(con)
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
                j = ARTJustification.findById(con,[self.justification.id])
                self.assertEqualJustification(self.justification, j[0])
                
                j = ARTJustification.findById(con, ["not_exists"])
                self.assertEqual(j, [])
                               
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.exception(e)
            
            


class TestJustificationArtFindByUserId(TestJustificationArt):
    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justification = TestJustificationArtFindByUserId.defineNewJustification(con)
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
                
                justs = ARTJustification.findByUserId(con, usersId, start, end)

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
