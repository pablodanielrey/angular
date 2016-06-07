import logging
import unittest
import sys
sys.path.append('../../python')

from testecono.TestEcono import TestEcono
from model.assistance.assistanceDao import AssistanceDAO
from model.users.users import User
from model.users.users import Telephone
from model.users.users import UserDAO

class TestAssistance(TestEcono):
    
    def setUp(self):
        super(TestAssistance, self).setUp()
        try:
            con = self.connection.get()
            try:
                AssistanceDAO._createSchema(con)
                con.commit()
                
            finally:
                self.connection.put(con)
            
        except Exception as e: 
            logging.error(str(e))
            
            
            
    def test_persist_user(self):
        try:
            con = self.connection.get()
            try:
                telephone = Telephone()
                telephone.type = "Móvil"
                telephone.number = "42123456"
                
                user = User()
                user.name = "Test Nom"
                user.lastname = "Test Ape"
                user.dni = "31012345"
                user.telephones = [ telephone ]
                
                UserDAO.persist(con, user)
                con.commit()
                
            finally:
                self.connection.put(con)
                
        except Exception as e: 
            logging.error(str(e))

    


if __name__ == '__main__':
    unittest.main()
