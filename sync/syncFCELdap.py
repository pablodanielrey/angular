# -*- coding: utf-8 -*-
import ldap
import ldap.modlist as modlist
import uuid
import sys
import psycopg2


user = sys.argv[1]
passw = sys.argv[2]
dbname = sys.argv[3]
dbuser = sys.argv[4]
dbpass = sys.argv[5]

l = ldap.initialize("ldap://127.0.0.1:3389")
l.protocol_version = ldap.VERSION3
l.simple_bind_s(user,passw);

try:
        result = l.search_s("ou=people,dc=econo",ldap.SCOPE_SUBTREE,"(x-dcsys-dni=*)",["uid","mail","x-dcsys-mail","x-dcsys-dni","sn","givenName","userPassword","x-dcsys-uuid","objectClass","l","co","x-dcsys-legajo"])
        if result == None:
                exit(1)


        con = psycopg2.connect(host='127.0.0.1', dbname=dbname, user=dbuser, password=dbpass)

        for dn,g in result:
                #print "\n"
                sys.stdout.write('.')

                userid = g['x-dcsys-uuid'][0]
                dni = g['x-dcsys-dni'][0]
                name = None
                lastname = None
                city = None
                country = None
                legajo = None
                mails = []
                userpassword = None

                #print g['x-dcsys-dni']

                if 'givenName' in g:
                    #print g['givenName']
                    name = g['givenName'][0]

                if 'sn' in g:
                    #print g['sn']
                    lastname = g['sn'][0]

                if 'x-dcsys-legajo' in g:
                    #print g['x-dcsys-legajo']
                    legajo = g['x-dcsys-legajo'][0]

                if 'mail' in g:
                    #print g['mail']
                    mails.append(g['mail'][0])


                if 'x-dcsys-mail' in g:
                    if g['x-dcsys-mail'][0] == 'correo ':
                        del g['x-dcsys-mail']
                    else:
                        #print g['x-dcsys-mail'][0]
                        mails.append(g['x-dcsys-mail'][0])


                userpassword = 'fgklnf409wdlkcm23f09hcsd'
                if 'userPassword' in g:
                    if g['userPassword'] == None or g['userPassword'] == '':
                        print "calve vacía"
                    else:
                        #print g['userPassword']
                        userpassword = g['userPassword'][0]
                else:
                    print "no tiene clave"

                groups = ''
                if 'x-dcsys-docente' in g['objectClass']:
                    groups += " docente"

                if 'x-dcsys-posgrado' in g['objectClass']:
                    groups += " posgrado"

                if 'x-dcsys-estudiante' in g['objectClass']:
                    groups += " alumno"

                #print groups


                # agrego a las tablas correspondientes la data del usuario recolectada.
                cur = con.cursor()

                # chequeo a ver que no exista ya en la base de datos
                cur.execute('select dni from profile.users where dni = %s', (dni,))
                data = cur.fetchone()
                if data != None:
                    continue


                # ignoro los legajos repetidos
                if legajo != None:
                    cur.execute('select student_number from students.users where student_number = %s', (legajo,))
                    data = cur.fetchone()
                    if data != None:
                        continue


                cur.execute('insert into profile.users (id,dni,name,lastname,city,country) values (%s,%s,%s,%s,%s,%s)', (userid,dni,name,lastname,city,country))
                cur.execute('insert into credentials.user_password (id,user_id,username,password) values (%s,%s,%s,%s)', (str(uuid.uuid4()),userid,dni,userpassword))

                for mail in mails:
                    confirmed = False
                    if 'econo.unlp.edu.ar' in mail:
                        confirmed = True
                    cur.execute('insert into profile.mails (id,user_id,email,confirmed,hash) values (%s,%s,%s,%s,%s)', (str(uuid.uuid4()), userid, mail, confirmed, ''))

                if legajo != None:
                    cur.execute('insert into students.users (id,student_number) values (%s,%s)', (userid,legajo))

                cur.execute('insert into au24.users (id,type) values (%s,%s)', (userid,groups))

                con.commit()

        print len(result)

except ldap.LDAPError, e:
        print e

finally:
        con.close();
        l.unbind_s()
