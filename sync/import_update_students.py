
import sys
import psycopg2
import csv
import uuid

user = sys.argv[1]
passw = sys.argv[2]
host = sys.argv[3]

db = psycopg2.connect(host=host, user=user, password=passw, dbname="dcsys")
cursor = db.cursor()

for a,n,l,d,b in csv.reader(sys.stdin):
    print 'actualizando %s' % d
    cursor.execute('select id from profile.users where dni = %s',(d,))
    iduser = cursor.fetchone()
    if iduser == None:
        print "no existe como usuario : %s" % d
        iduser = str(uuid.uuid4())
        cursor.execute('insert into profile.users (id,dni,name,lastname) values (%s,%s,%s,%s)',(iduser,d,n,a))
        cursor.execute('insert into credentials.user_password (id,user_id,username,password) values (%s,%s,%s,%s)', (str(uuid.uuid4()),iduser,d,d))
        cursor.execute('insert into students.users (id,student_number) values (%s,%s)', (iduser,l))
        cursor.execute('insert into au24.users (id,type) values (%s,%s)', (iduser,'alumno ingresante'))
        db.commit()
        continue

    cursor.execute('select id from students.users where id = %s',(iduser,))
    if len(cursor.fetchall()) <= 0:
        print "insertando alumno %s" % d
        cursor.execute('insert into students.users (id,student_number) values (%s,%s)',(iduser,l))
    else:
        print "actualizando alumno %s" % d
        cursor.execute('update students.users set student_number = %s where id = %s',(l,d))

db.commit()
