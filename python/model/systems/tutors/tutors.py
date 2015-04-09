# -*- coding: utf-8 -*-

import uuid, logging

class Tutors:

    def list(self,con):
        cur = con.cursor()
        cur.execute('select user_id, date, student_number, dni, name, lastname, type, created from tutors.tutors')
        data = cur.fetchall()
        tutors = []
        for d in data:
            tutor = self.convertToDict(d)
            tutors.append(tutor)
        return tutors


    def persist(self,con,tutor):
        student = tutor['student']
        params = (str(uuid.uuid4()), tutor['userId'], tutor['date'], student['studentNumber'], student['dni'], student['name'], student['lastname'], tutor['type'])
        cur = con.cursor()
        cur.execute('insert into tutors.tutors (id,user_id,date,student_number,dni,name,lastname,type) values (%s,%s,%s,%s,%s,%s,%s,%s)',params)


    def convertToDict(self,s):
        student = {
            'studentNumber':s[2],
            'dni':s[3],
            'name':s[4],
            'lastname':s[5]
        }
        tutor = {
            'userId':s[0],
            'date':s[1],
            'student':student,
            'type':s[6],
            'created':s[7]
        }
        return tutor
