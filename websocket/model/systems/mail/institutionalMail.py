# -*- coding: utf-8 -*-
import psycopg2
from model.objectView import ObjectView

class InstitutionalMail:

    def persistMail(self,con,user):
        if (self.findMail(con,user['id'])) == None:
            params = (user['id'],)
            cur = con.cursor()
            cur.execute('insert into mail.users (id) values (%s)',params)

    def deleteMail(self,con,id):
        cur = con.cursor()
        cur.execute('delete from mail.users where id = %s',(id,))

    def findMail(self,con,id):
        cur = con.cursor()
        cur.execute('select id from mail.users where id = %s',(id,))
        m = cur.fetchone()
        if m:
            return self.convertToDict(m)
        else:
            return None

    def convertToDict(self,m):
        userMail = {
            'id':m[0]
        }
        return userMail
