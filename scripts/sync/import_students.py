
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

for n,a,d,m in csv.reader(sys.stdin):
    print "teniendo en cuenta {}".format(d)
    cursor.execute('select id from profile.users where dni = %s',(d,))
    if cursor.rowcount > 0:
        iduser = cursor.fetchone()
        if iduser is None:
            print "no existe como usuario : %s" % d
            iduser = str(uuid.uuid4())
            cursor.execute('insert into profile.users (id,dni,name,lastname) values (%s,%s,%s,%s)',(iduser,d,n,a))
            cursor.execute('insert into credentials.user_password (id,user_id,username,password) values (%s,%s,%s,%s)', (str(uuid.uuid4()),iduser,d,d))
            cursor.execute('insert into students.users (id,student_number) values (%s,%s)', (iduser,''))
            cursor.execute('insert into au24.users (id,type) values (%s,%s)', (iduser,'alumno'))
            ncreados = ncreados + 1
            creados.write('{};{};{}\n'.format(a,n,d))
        else:
            errores.write('{};{};{}\n'.format(a,n,d))
    else:
        nerrores = nerrores + 1
        errores.write('{};{};{}\n'.format(a,n,d))

#db.commit()
db.rollback()

print "creados : {}".format(ncreados)
print "errores : {}".format(nerrores)
