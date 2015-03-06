# -*- coding: utf-8 -*-
class Tutors:

    def listTutorData(self,con):
        cur = con.cursor()
        cur.execute('select user_id, date, student_number, type from tutors.tutors')
        data = cur.fetchall()
        tutors = []
        for d in data:
            tutor = convertToDict(d)
            tutors.append(tutor)
        return tutors


    def persistTutorData(self,con,tutor):
        params = (str(uuid.uuid4()), tutor['userId'], tutor['date'], tutor['studentNumber'])
        cur = con.cursor()
        cur.execute('insert into tutors.tutors (id,user_id,date,student_number) values (%s,%s,%s,%s)',params)


    def convertToDict(self,s):
        tutor = {
            'userId':s[0],
            'date':s[1],
            'studentNumber':s[2],
            'type':s[3]
        }
        return tutor
