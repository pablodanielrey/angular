import logging
import unittest
import sys
sys.path.append('../../python')

from testecono.TestEcono import TestEcono
from model.users.users import User
from model.users.users import Telephone
from model.users.users import UserDAO


class TestUser(TestEcono):
    
    def setUp(self):
        super(TestUser, self).setUp()
        try:
            con = self.connection.get()
            try:
                UserDAO._createSchema(con)
                con.commit()
       
            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.error(str(e))
            
    def defineUser(self):
        telephone = Telephone()
        telephone.type = "Móvil"
        telephone.number = "42123456"
        
        user = User()
        user.name = "Test Nom"
        user.lastname = "Test Ape"
        user.dni = "31012345"
        user.telephones = [ telephone ]
        
        return user           


    def defineUserAndPersist(self):
        user = self.defineUser()
      
        con = self.connection.get()

        try:
            u = User.findByDni(con, user.dni)

            if u is not None:
                user.id = u[0]

            uid = user.persist(con)
            con.commit()

            return uid, user
            
        finally:
            self.connection.put(con)
            
            
    def assertEqualTelephones(self, telephone, telephone2):
        self.assertEqual(telephone.type, telephone2.type)


    def assertEqualUsers(self, user, user2):
        self.assertEqual(user.name, user2.name)
        self.assertEqual(user.lastname, user2.lastname)
        self.assertEqual(user.dni, user2.dni)
        self.assertEqual(len(user.telephones), len(user2.telephones))
        for t1, t2 in zip(user.telephones, user2.telephones):
           self.assertEqualTelephones(t1,t2)





class TestUserPersist(TestUser):
    
    def setUp(self):
        super(TestUserPersist, self).setUp()
        self.user = self.defineNewUser()

    def defineNewUser(self):
        user = self.defineUser()
      
        con = self.connection.get()

        try:
            uid = User.findByDni(con, user.dni)
            users = User.findById(con, [uid[0]])
            u = users[0]

            if(u is not None):
                u.delete(con)
                con.commit()
            
        finally:
            self.connection.put(con)

        return user    

            
    def test_persist(self):
        try:
            con = self.connection.get()
            try:
                ##### insertar #####
                self.user.persist(con)
                con.commit()
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

            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.error(str(e))
            
            
            
            
            
            
            
            
            
class TestUserFindById(TestUser):
    
    def setUp(self):
        super(TestUserFindById, self).setUp()
        self.user_id, self.user = self.defineUserAndPersist()

    def test_find_by_id(self):
        try:
            con = self.connection.get()
            try:
                u = User.findById(con,[self.user.id])
                self.assertEqualUsers(self.user, u[0])
                
                u = User.findById(con, ["not_exists"])
                self.assertEqual(u, [])
                
                               
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.error(str(e))









class TestUserFindAll(TestUser):
    
    def setUp(self):
        super(TestUserFindAll, self).setUp()
        self.user_id, self.user = self.defineUserAndPersist()

 
 
    def test_find_all(self):
        try:
            con = self.connection.get()
            uTuple = (self.user_id, self.user.version)
            try:
                u = User.findAll(con)
                self.assertIn(uTuple, u)
                
                uTupleNotExists = ("id", "0")
                self.assertNotIn(uTupleNotExists, u)
                
                               
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.error(str(e))
            
            
            
            
            
            
            
class TestUserDelete(TestUser):
    
    def setUp(self):
        super(TestUserDelete, self).setUp()
        self.user_id, self.user = self.defineUserAndPersist()

 
 
    def test_delete(self):
        try:
            con = self.connection.get()

            try:                
                self.user.delete(con)
                con.commit()
                
                u = User.findById(con, [self.user_id])
                self.assertEqual(u, [])
                               
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.error(str(e))

