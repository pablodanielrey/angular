# -*- coding: utf-8 -*-
'''
Agregar usuarios en windows y establecer clave del fce
Utilizar findAllOffices para consultar los id de oficinas

python3 addUserPasswordWindows.py "officeId"

python3 findAllOffices.py #consultar oficinas para buscar un determinado id
python3 addUserPasswordWindows.py a645e297-cc8e-43eb-a0a9-ce3484cc80d6
'''

import connection
import groups
import sys
import users
import subprocess

import logging
logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    con = connection.getConnection()
    try:
        officeId = sys.argv[1]

        office = groups.OfficeDAO.findById(con, officeId)

        if(office.name):
            print("GRUPO: " + office.name)

        for userId in office.users:
          userInfo = users.UserPasswordDAO.findByUserId(con, userId)

          for userData in userInfo:
              if userData.username and userData.password:
                  print("USUARIO: " + userData.username)
                  cmd = "NET user " + userData.username + " " + userData.password + " /add /passwordreq:yes"
                  if(sys.version_info.major == 3) and (sys.version_info.minor > 4):
                    cp = subprocess.run(cmd, shell=True)
                  else:
                    cp = subprocess.call(cmd, shell=True)

    finally:
        connection.closeConnection(con)
