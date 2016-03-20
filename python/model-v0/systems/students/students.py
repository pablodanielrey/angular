# -*- coding: utf-8 -*-


class Students:

    def persist(self, con, student):
        id = student['id']
        params = (student['studentNumber'], student['condition'], id)
        cur = con.cursor()
        cur.execute('select id from students.users where id = %s', (id,))
        if cur.rowcount <= 0:
            cur.execute('insert into students.users (student_number, condition, id) values (%s,%s,%s)', params)
        else:
            cur.execute('update students.users set student_number = %s, condition = %s where id = %s', params)

    def findById(self, con, id):
        cur = con.cursor()
        cur.execute('select id,student_number,condition from students.users where id = %s', (id,))
        s = cur.fetchone()
        if s:
            return self._convertToDict(s)
        else:
            return None

    def findByNumber(self, con, n):
        cur = con.cursor()
        cur.execute('select id, student_number, condition from students.users where student_number = %s', (n,))
        s = cur.fetchone()
        if (s is None):
            return None
        return self._convertToDict(s)

    def _convertToDict(self, s):
        student = {
            'id': s[0],
            'studentNumber': s[1],
            'condition': s[2]
        }
        return student
