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


"""
    def createLaboralInsertion(self,con,laboralInsertion):
        params = (laboralInsertion['id'],laboralInsertion['cv'],laboralInsertion['residir'],laboralInsertion['viajar'])
        cur = con.cursor()
        cur.execute("insert into laboral_insertion.users (id,cv,reside,travel) values (%s,%s,%s,%s)",params)


    def updateLaboralInsertion(self,con,li):
        laboralInsertion = ObjectView(li)
        params = (laboralInsertion.cv,laboralInsertion.residir,laboralInsertion.viajar,laboralInsertion.id)
        cur = con.cursor()
        cur.execute('update laboral_insertion.users set cv = %s,reside = %s,travel = %s where id = %s',params)
"""


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

    def createLanguage(self,con,language):
        params = (language['id'],language['user_id'],language['name'],language['level'])
        cur = con.cursor()
        cur.execute('insert into laboral_insertion.languages (id,user_id,name,level) values(%s,%s,%s,%s)',params)

    def updateLanguage(self,con,l):
        language = ObjectView(l)
        params = (language.user_id,language.name,language.level,language.id)
        cur = con.cursor()
        cur.execute('update laboral_insertion.languages set user_id = %s, name = %s, level = %s where id = %s',params)

    def deleteLanguage(self,con,id):
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.languages where id = %s',(id))

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
            'aproved':d[4],
            'average1':d[5],
            'average2':d[6],
            'work_type':d[7]
        }
        return degree

    def createDegree(self,con,d):
        degree = ObjectView(d)
        params = (degree.id,degree.user_id,degree.name,degree.curses,degree.aproved,degree.average1,degree.average2,degree.work_type)
        cur = con.cursor()
        cur.execute('insert into laboral_insertion.degree (id,user_id,name,curses,aproved,average1,average2,work_type) values(%s,%s,%s,%s,%s,%s,%s,%s)',params)

    def updateDegree(self,con,d):
        degree = ObjectView(d)
        params = (degree.user_id,degree.name,degree.curses,degree.aproved,degree.average1,degree.average2,degree.work_type,degree.id)
        cur = con.cursor()
        cur.execute('update laboral_insertion.degree set user_id = %s, name = %s, curses = %s, aproved = %s, average1 = %s, average2 = %s, work_type = %s where id = %s',params)

    def deleteDegree(self,con,id):
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.degree where id = %s',(id))

    def findDegree(self,con,id):
        cur = con.cursor()
        cur.execute('select id,user_id,name,curses,aproved,average1,average2,work_type from laboral_insertion.degree where id = %s',(id))
        degree = cur.fetchone()
        if degree != None:
            return self.convertDegreeToDict(degree)
        else:
            return None

    def listDegrees(self,con,user_id):
        cur = con.cursor()
        cur.execute('select id,user_id,name,curses,aproved,average1,average2,work_type from laboral_insertion.degree where user_id = %s',(user_id))
        data = cur.fetchall()
        degrees = []
        for d in data:
            degrees.append(self.convertDegreeToDict(d))
        return degrees
