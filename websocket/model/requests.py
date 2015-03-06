# -*- coding: utf-8 -*-
import psycopg2

class Requests:

    def __init__(self):
        self.registerQuery = 'select id,dni,student_number,name,lastname,email,reason,password,hash,confirmed from account_requests.requests'


    def convertToDict(self, d):
        r = {
            'id':d[0],
            'dni':d[1],
            'studentNumber':d[2],
            'name':d[3],
            'lastname':d[4],
            'email':d[5],
            'reason':d[6],
            'password':d[7],
            'hash':d[8],
            'confirmed':d[9]
        }
        return r


    def listRequests(self, con):
        cur = con.cursor()
        cur.execute(self.registerQuery);
        data = cur.fetchall();
        if data == None:
            return []

        ''' transformo a diccionario la respuesta '''
        rdata = []
        for d in data:
            rdata.append(self.convertToDict(d))

        return rdata


    def findRequest(self, con, id):
        cur = con.cursor()
        cur.execute(self.registerQuery + ' where id = %s',(id,));
        d = cur.fetchone()
        if d == None:
            return None

        ''' transformo a diccionario la respuesta '''
        rdata = self.convertToDict(d)
        return rdata


    def findRequestByHash(self, con, hash):
        cur = con.cursor()
        cur.execute(self.registerQuery + ' where hash = %s',(hash,));
        d = cur.fetchone()
        if d == None:
            return None

        ''' transformo a diccionario la respuesta '''
        rdata = self.convertToDict(d)
        return rdata


    def confirmRequest(self, con, rid):
        cur = con.cursor()
        cur.execute('update account_requests.requests set confirmed = true where id = %s', (rid,))


    def createRequest(self, con, req):
        rreq = (req['id'],req['dni'],req['studentNumber'],req['name'],req['lastname'],req['email'],req['reason'],req['password'],req['hash'])
        cur = con.cursor()
        cur.execute('insert into account_requests.requests (id,dni,student_number,name,lastname,email,reason,password,hash) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', rreq)


    def removeRequest(self, con, rid):
        cur = con.cursor()
        cur.execute('delete from account_requests.requests where id = %s', (rid,))
