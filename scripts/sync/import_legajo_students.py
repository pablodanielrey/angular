
import sys
import psycopg2
import csv
import uuid

user = sys.argv[1]
passw = sys.argv[2]
host = sys.argv[3]

db = psycopg2.connect(host=host, user=user, password=passw, dbname="dcsys")
cursor = db.cursor()

nerrores = 0
errores = open('/tmp/errores.txt','w')

ncreados = 0
creados = open('/tmp/creados.txt','w')

nactualizados = 0
actualizados = open('/tmp/actualizados.txt','w')

for carr,a,n,l,d,b in csv.reader(sys.stdin):
    cursor.execute('select id from profile.users where dni = %s',(d,))
    if cursor.rowcount > 0:
        iduser = cursor.fetchone()
        if iduser is None:
            print "no existe como usuario : %s" % d
            iduser = str(uuid.uuid4())
            cursor.execute('insert into profile.users (id,dni,name,lastname) values (%s,%s,%s,%s)',(iduser,d,n,a))
            cursor.execute('insert into credentials.user_password (id,user_id,username,password) values (%s,%s,%s,%s)', (str(uuid.uuid4()),iduser,d,d))
            cursor.execute('insert into students.users (id,student_number) values (%s,%s)', (iduser,l))
            cursor.execute('insert into au24.users (id,type) values (%s,%s)', (iduser,'alumno ingresante'))
            #db.commit()
            ncreados = ncreados + 1
            creados.write('{};{};{};{}\n'.format(a,n,l,d))
            db.commit()
            continue

    cursor.execute('select id from students.users where id = %s',(iduser,))
    if cursor.rowcount <= 0:
        print "insertando alumno %s" % d
        cursor.execute('select id from students.users where student_number = %s', (l,))
        if cursor.rowcount > 0:
            a1 = cursor.fetchone()
            cursor.execute('select name, lastname, dni from profile.users where id = %s', (a1[0],))
            a1 = cursor.fetchone()
            errores.write('{};{};{};{}\n'.format(l, a1[0], a1[1], a1[2]))
            nerrores = nerrores + 1
            continue
        cursor.execute('insert into students.users (id,student_number) values (%s,%s)',(iduser,l))
        ncreados = ncreados + 1
        actualizados.write('{};{};{};{}\n'.format(a,n,l,d))
    else:
        print "actualizando alumno %s" % d
        cursor.execute('update students.users set student_number = %s where id = %s',(l,d))
        nactualizados = nactualizados + 1
        actualizados.write('{};{};{};{}\n'.format(a,n,l,d))

#db.commit()
db.commit()

print "actualizados : {}".format(nactualizados)
print "creados : {}".format(ncreados)
print "errores : {}".format(nerrores)
