# -*- coding: utf-8 -*-
import ldap
import ldap.modlist as modlist
import uuid
import sys
import psycopg2


dbname = sys.argv[1]
dbuser = sys.argv[2]
dbpass = sys.argv[3]

dni = sys.argv[4]
name = sys.argv[5]
lastname = sys.argv[6]
legajo = sys.argv[7]
userpassword = sys.argv[7]
mail = sys.argv[8]
userid = str(uuid.uuid4())
city = None
country = None


con = psycopg2.connect(host='163.10.17.80', dbname=dbname, user=dbuser, password=dbpass)

# agrego a las tablas correspondientes la data del usuario recolectada.
cur = con.cursor()

# chequeo a ver que no exista ya en la base de datos
cur.execute('select dni from profile.users where dni = %s', (dni,))
data = cur.fetchone()
if data != None:
    print "ya existe"
    sys.exit(1)


# ignoro los legajos repetidos
if legajo != None:
    cur.execute('select student_number from students.users where student_number = %s', (legajo,))
    data = cur.fetchone()
    if data != None:
        print "legajo ya existe"
        sys.exit(1)


cur.execute('insert into profile.users (id,dni,name,lastname,city,country) values (%s,%s,%s,%s,%s,%s)', (userid,dni,name,lastname,city,country))
cur.execute('insert into credentials.user_password (id,user_id,username,password) values (%s,%s,%s,%s)', (str(uuid.uuid4()),userid,dni,userpassword))

confirmed = False
cur.execute('insert into profile.mails (id,user_id,email,confirmed,hash) values (%s,%s,%s,%s,%s)', (str(uuid.uuid4()), userid, mail, confirmed, ''))

if legajo != None:
    cur.execute('insert into students.users (id,student_number) values (%s,%s)', (userid,legajo))

cur.execute('insert into au24.users (id,type) values (%s,%s)', (userid,'alumno ingresante'))

con.commit()
con.close();
