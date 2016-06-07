# -*- coding: utf-8 -*-

class Systems:

    def listSystems(self,con):
        cur = con.cursor()
        cur.execute('select id,name,config from systems.systems')
        ss = cur.fetchall()
        systems = []
        for s in ss:
            systems.append(self.convertToDict(s))
        return systems

    def convertToDict(self,r):
        d = {
            'id':r[0],
            'name':r[1],
            'config':r[2]
        }
        return d
