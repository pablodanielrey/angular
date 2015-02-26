import psycopg2
from model.objectView import ObjectView

class LaboralInsertion:


    def persistLaboralInsertion(self,con,data):
        if findLaboralInsertion(con,data['id']) == None:
            params = (data['id'],psycopg2.Binary(data['cv']),data['reside'],data['travel'])
            cur = con.cursor()
            cur.execute("insert into laboral_insertion.users (id,cv,reside,travel) values (%s,%s,%s,%s)",params)
        else:
            params = (psycopg2.Binary(data['cv']),data['reside'],data['travel'],data[id])
            cur = con.cursor()
            cur.execute('update laboral_insertion.users set cv = %s,reside = %s,travel = %s where id = %s',params)


    def findLaboralInsertion(self,con,id):
        cur = con.cursor()
        cur.execute('select id,cv,reside,travel from laboral_insertion.users where id = %s',(id))
        li = cur.fetchone()
        if li:
            return self.convertUserToDict(li)
        else:
            return None

    def findAll(self,con):
        cur = con.cursor()
        cur.execute('select id,cv,reside,travel from laboral_insertion.users where id = %s',(id))
        data = cur.fetchall()
        laboralInsertions = []
        for li in data:
            laboralInsertion = self.convertUserToDict(li)
            laboralInsertions.append(laboralInsertion)
        return laboralInsertions

    def convertUserToDict(self,li):
        laboralInsertion = {
            'id':li[0],
            'cv':li[1],
            'reside':li[2],
            'travel':li[3]
        }
        return laboralInsertion

    """-------------------------------"""

    def convertLanguageToDict(self,l):
        language = {
            'id':l[0],
            'user_id':l[1],
            'name':l[2],
            'level':l[3]
        }
        return language

    def persistLanguage(self,con,data):
        if findLanguage(con,data['id']) == None:
            params = (data['id'],data['user_id'],data['name'],data['level'])
            cur = con.cursor()
            cur.execute('insert into laboral_insertion.languages (id,user_id,name,level) values(%s,%s,%s,%s)',params)
        else:
            params = (data['user_id'],data['name'],data['level'],data['id'])
            cur = con.cursor()
            cur.execute('update laboral_insertion.languages set user_id = %s, name = %s, level = %s where id = %s',params)

    def deleteLanguage(self,con,id):
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.languages where id = %s',(id))

    def deleteLanguages(self,con,user_id):
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.languages where user_id = %s',(user_id))

    def findLanguage(self,con,id):
        cur = con.cursor()
        cur.execute('select id, user_id, name, level from laboral_insertion.languages where id = %s',(id))
        language = cur.fetchone()
        if language != None:
            return self.convertLanguageToDict(language)
        else:
            return None

    def listLanguages(self,con,user_id):
        cur = con.cursor()
        cur.execute('select id, user_id, name, level from laboral_insertion.languages where user_id = %s',(user_id))
        data = cur.fetchall()
        languages = []
        for d in data:
            languages.append(self.convertLanguageToDict(d))
        return languages

    """-------------------------------"""

    def convertDegreeToDict(self,d):
        degree = {
            'id':d[0],
            'user_id':d[1],
            'name':d[2],
            'curses':d[3],
            'average1':d[4],
            'average2':d[5],
            'work_type':d[6]
        }
        return degree

    def persistDegree(self,con,data):
        if findDegree(con,data['id']) == None:
            params = (degree['id'],degree['user_id'],degree['name'],degree['curses'],degree['average1'],degree['average2'],degree['work_type'])
            cur = con.cursor()
            cur.execute('insert into laboral_insertion.degree (id,user_id,name,curses,average1,average2,work_type) values(%s,%s,%s,%s,%s,%s,%s)',params)
        else:
            params = (degree['user_id'],degree['name'],degree['curses'],degree['average1'],degree['average2'],degree['work_type'],degree['id'])
            cur = con.cursor()
            cur.execute('update laboral_insertion.degree set user_id = %s, name = %s, curses = %s, average1 = %s, average2 = %s, work_type = %s where id = %s',params)

    def deleteDegree(self,con,id):
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.degree where id = %s',(id))


    def deleteDegrees(self,con,user_id):
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.degree where user_id = %s',(user_id))


    def findDegree(self,con,id):
        cur = con.cursor()
        cur.execute('select id,user_id,name,curses,average1,average2,work_type from laboral_insertion.degree where id = %s',(id))
        degree = cur.fetchone()
        if degree != None:
            return self.convertDegreeToDict(degree)
        else:
            return None

    def listDegrees(self,con,user_id):
        cur = con.cursor()
        cur.execute('select id,user_id,name,curses,average1,average2,work_type from laboral_insertion.degree where user_id = %s',(user_id))
        data = cur.fetchall()
        degrees = []
        for d in data:
            degrees.append(self.convertDegreeToDict(d))
        return degrees
