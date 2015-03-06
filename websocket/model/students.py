# -*- coding: utf-8 -*-
import psycopg2
from model.objectView import ObjectView

class Students:

    def createStudent(self,con,student):
        params = (student['id'],student['studentNumber'],student['condition'])
        cur = con.cursor()
        cur.execute('insert into students.users (id,student_number,condition) values (%s,%s,%s)',params)


    def findStudent(self,con,id):
        cur = con.cursor()
        cur.execute('select id,student_number,condition from students.users where id = %s',(id,))
        s = cur.fetchone()
        if s:
            return self.convertToDict(s)
        else:
            return None

    def findStudentByNumber(self,con,n):
        cur = con.cursor()
        cur.execute('select id,student_number,condition from students.users where student_number = %s',(n,))
        s = cur.fetchone()
        return self.convertToDict(s)


    def findAll(self,con):
        cur = con.cursor()
        cur.execute('select id,student_number,condition from students.users')
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

    """
    " updateStudent
    " @param con Conexion con la base de datos
    " @param studentDic Diccionario con los datos del estudiante
    """
    def updateStudent(self,con,studentDic):
        student = ObjectView(studentDic)
        studentTuple = (student.studentNumber, student.condition)
        cur = con.cursor()
        cur.execute('update students.users set student_number = %s, condition = %s where id = %s', rreq)
        if cur.rowcount <= 0:
            raise Exception()
