# -*- coding: utf-8 -*-
import uuid

class Groups:

    def createGroup(self,con,group):
        cur = con.cursor()
        cur.execute('insert into groups (id,system_id,name) values (%s,%s,%s)',(group.id,group.systemId,group.name))

    def updateGroup(self,con,group):
        cur = con.cursor()
        cur.execute('update groups set name = %s where id = %s',(group.name,group.id))

    def addMembers(self,con,id,members):
        cur = con.cursor()
        for uid in members:
            cur.execute('insert into groups_users (group_id,user_id) values (%s,%s)',(id,uid))


    def removeMembers(self,con,id,members):
        cur = con.cursor()
        for uid in members:
            cur.execute('delete from groups_users where group_id = %s and user_id = %s',(id,uid))

    def findMembers(self,con,id):
        cur = con.cursor()
        cur.execute('select user_id from groups_users where group_id = %s',(id,))
        data = cur.fetchall()
        rdata = []
        for d in data:
            rdata.append(d[0])
        return rdata


    def findGroup(self,con,id):
        cur = con.cursor()
        cur.execute('select id,system_id,name from groups where id = %s',(id,))
        g = cur.fetchone()
        group = self.convertToDict(g)
        return group


    def listGroups(self, con):
        cur = con.cursor()
        cur.execute('select id,system_id,name from groups')
        data = cur.fetchall()
        rdata = []
        for d in data:
            rdata.append(self.convertToDict(d))
        return rdata


    ''' transformo a diccionario las respuestas de psycopg2'''
    def convertToDict(self,d):
        rdata = {
                'id':d[0],
                'systemId':d[1],
                'name':d[2]
            }
        return rdata
