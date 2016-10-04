# -*- coding: utf-8 -*-
'''
Crear o modificar archivo de usuarios con formato radius, se crea un archivo por grupo consultado
Utilizar findAllOffices para consultar los id de oficinas
Establecer en el script las variables "directory" y "filename" deseadas

python3 addUserFileRadius.py "officeId"

python3 findAllOffices.py #consultar oficinas para buscar un determinado id
python3 addUserFileRadius.py a645e297-cc8e-43eb-a0a9-ce3484cc80d6
'''

import connection
import groups
import sys
import users
import os

directory = "" 


if __name__ == '__main__':
    con = connection.getConnection()
    try:

        #***** consultar oficina *****
        officeId = sys.argv[1]

        office = groups.OfficeDAO.findById(con, officeId)
        if not office:
            raise Exception("No existe grupo")
            
        print("GRUPO: " + office.name)

        if not office.users:
            raise Exception("No existen usuarios")
            
        
        #***** abrir archivo *****
        filename = "users" + officeId
        
        f = open(os.path.join(directory, filename), "w")
        
        if directory:
            if not os.path.exists(directory):
                os.makedirs(directory)      
            
            f = open(os.path.join(directory, filename), "w")
        else:
            f = open(filename, "w")
        


        #***** consultar usuarios y escribir archivo *****
        f.write("#" + office.name)
        
        try:      
            for userId in office.users:
                userInfo = users.UserPasswordDAO.findByUserId(con, userId)
                if not userInfo:
                    print("USUARIO NO AGREGADO: " + userId + " (SIN DATOS)")
                for userData in userInfo:
                    if userData.username and userData.password:
                        print("USUARIO: " + userData.username)
                        
                        f.write("""
%s Cleartext-Password := "%s"
	Service-Type = Framed-User,
	Framed-Protocol = PPP,
	Framed-Compression = Van-Jacobsen-TCP-IP
""" % (userData.username, userData.password))
                    else: 
                        print("USUARIO NO AGREGADO: " + userData.username + " (SIN CLAVE)")

        finally:
            f.close()

                          
    finally:
        connection.closeConnection(con)
             


    
    


