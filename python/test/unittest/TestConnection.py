import os
from os import listdir
from os.path import isfile, join

import unittest
import inject
inject.configure()

import sys
sys.path.append('../../../python')


from model.registry import Registry
from model.connection.connection import Connection
from model.users.users import UserDAO
from model.users.users import UserPasswordDAO
from model.files.files import FileDAO
from model.users.users import MailDAO
from model.users.users import StudentDAO

class TestConnection(unittest.TestCase):
      
  def test_create_database(self):
    try:
      reg = inject.instance(Registry)
      
      registrySection = reg.getRegistry('dcsys2')

      conn = Connection(registrySection)
      
      con = conn.get()
      
      #FileDAO._createSchema(con)
      #UserDAO._createSchema(con)
      #UserPasswordDAO._createSchema(con)
      #MailDAO._createSchema(con)
      StudentDAO._createSchema(con)
      
      #UserDAO.findByDni(con, "31073351")
           
      #uid, v = UserDAO.findByDni(con, "31073351")
      
      #print("uid"  + uid)
      #print("value"  + v)

      
      


      
    except Exception as e:
      print(str(e))


  

if __name__ == '__main__':
    unittest.main()
