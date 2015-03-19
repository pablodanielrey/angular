# -*- coding: utf-8 -*-

import uuid

class Tutors:

    def list(self,con):
        cur = con.cursor()
        cur.execute('select user_id, date, student_number, type from tutors.tutors')
        data = cur.fetchall()
        tutors = []
        for d in data:
            tutor = convertToDict(d)
            tutors.append(tutor)
        return tutors


    def persist(self,con,tutor):
        params = (str(uuid.uuid4()), tutor['userId'], tutor['date'], tutor['studentNumber'], tutor['type'])
        cur = con.cursor()
        cur.execute('insert into tutors.tutors (id,user_id,date,student_number,type) values (%s,%s,%s,%s,%s)',params)


    def convertToDict(self,s):
        tutor = {
            'userId':s[0],
            'date':s[1],
            'studentNumber':s[2],
            'type':s[3]
        }
        return tutor
