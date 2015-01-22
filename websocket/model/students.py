
import psycopg2

class Students:

    def createStudent(self,con,student):
        params = (student['id'],student['studentNumber'],student['condition'])
        cur = con.cursor()
        cur.execute('insert into students (id,student_number,condition) values (%s,%s,%s)',params)


    def findStudent(self,con,id):
        cur = con.cursor()
        cur.execute('select id,student_number,condition from students where id = %s',(id,))
        s = cur.fetchone()
        if s:
            return self.convertToDict(s)
        else:
            return None

    def findStudentByNumber(self,con,n):
        cur = con.cursor()
        cur.execute('select id,student_number,condition from students where student_number = %s',(n,))
        s = cur.fetchone()
        return self.convertToDict(s)


    def findAll(self,con):
        cur = con.cursor()
        cur.execute('select id,student_number,condition from students where id = %s',(id,))
        ss = cur.fetchall()
        students = []
        for s in ss:
            student = self.convertToDict(s)
            students.append(student)
        return students

    def convertToDict(self,s):
        student = {
            'id':s[0],
            'studentNumber':s[1],
            'condition':s[2]
        }
        return student
