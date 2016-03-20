# -*- coding: utf-8 -*-
import psycopg2
from model.objectView import ObjectView

class Domain:

    def persistDomain(self,con,user):
        if (self.findDomain(con,user['id'])) == None:
            params = (user['id'],)
            cur = con.cursor()
            cur.execute('insert into domain.users (id) values (%s)',params)

    def deleteDomain(self,con,id):
        cur = con.cursor()
        cur.execute('delete from domain.users where id = %s',(id,))

    def findDomain(self,con,id):
        cur = con.cursor()
        cur.execute('select id from domain.users where id = %s',(id,))
        d = cur.fetchone()
        if d:
            return self.convertToDict(d)
        else:
            return None

    def convertToDict(self,d):
        userDomain = {
            'id':d[0]
        }
        return userDomain
