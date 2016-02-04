# -*- coding: utf-8 -*-
'''
    Obtiene los usuarios de la base de datos principal que pertenecen a la oficina Cedlas y los sincroniza con el linux actual.
    Tambien actualiza la clave en el samba
'''

import connection
import groups
import sys
import users
import subprocess
from subprocess import PIPE



import logging
logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    con = connection.getConnection()
    try:
        officeId = sys.argv[1]

        office = groups.OfficeDAO.findById(con, officeId)
      
        for userId in office.users:
          userInfo = users.UserPasswordDAO.findByUserId(con, userId)
          for userData in userInfo:
              if userData.username and userData.password:
                  cmd = "NET user " + userData.username + " " + userData.password + " /add /passwordreq:yes" 
                  if(sys.version_info.major == 3) and (sys.version_info.minor > 4):
                    cp = subprocess.run(cmd, shell=True)
                  else:
                    cp = subprocess.call(cmd, shell=True)
                    
                  logging.info(cp)

    finally:
        connection.closeConnection(con)
             


    
    


