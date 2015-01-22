# -*- coding: utf-8 -*-
import psycopg2

class Requests:

    def listRequests(self, con):
        cur = con.cursor()
        cur.execute('select id,dni,name,lastname,email,reason from account_requests');
        data = cur.fetchall();
        if data == None:
            return []

        ''' transformo a diccionario la respuesta '''
        rdata = []
        for d in data:
            rdata.append({
                'id':d[0],
                'dni':d[1],
                'name':d[2],
                'lastname':d[3],
                'email':d[4],
                'reason':d[5]
            })

        return rdata


    def findRequest(self, con, id):
        cur = con.cursor()
        cur.execute('select id,dni,name,lastname,email,reason from account_requests where id = %s',(id,));
        d = cur.fetchone()
        if d == None:
            return None

        ''' transformo a diccionario la respuesta '''
        rdata = {
            'id':d[0],
            'dni':d[1],
            'name':d[2],
            'lastname':d[3],
            'email':d[4],
            'reason':d[5]
        }
        return rdata


    def createRequest(self, con, req):
        rreq = (req['id'],req['dni'],req['name'],req['lastname'],req['email'],req['reason'])
        cur = con.cursor()
        cur.execute('insert into account_requests (id,dni,name,lastname,email,reason) values (%s,%s,%s,%s,%s,%s)', rreq)

    def removeRequest(self, con, rid):
        cur = con.cursor()
        cur.execute('delete from account_requests where id = %s', (rid,))
