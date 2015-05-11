import psycopg2
import logging
from model.objectView import ObjectView

class LaboralInsertion:

    """
        método usado por los administradores para obtener la info de inserción laboral.
    """
    def getLaboralInsertionData(self,con):
        data = self.findAll(con)
        for d in data:
            userId = d['id']
            langs = self.listLanguages(con,userId)
            d['languages'] = langs

            degrees = self.listDegrees(con,userId)
            d['degrees'] = degrees

        return data


    def acceptTermsAndConditions(self,con,id):

        cur = con.cursor()
        cur.execute('select accepted_conditions from laboral_insertion.users where id = %s',(id,))
        result = cur.fetchone()
        params = (True, id)
        if result != None:
            cur.execute('update laboral_insertion.users set accepted_conditions = %s where id = %s',params)
        else:
            cur.execute('INSERT INTO laboral_insertion.users (accepted_conditions, id) VALUES (%s, %s)',params)

    def checkTermsAndConditions(self,con,id):
        cur = con.cursor()
        cur.execute('select accepted_conditions from laboral_insertion.users where id = %s',(id,))
        language = cur.fetchone()
        if language != None:
            return language[0]
        else:
            return False

    def findLaboralInsertion(self,con,id):
        cur = con.cursor()
        cur.execute('select id,reside,travel from laboral_insertion.users where id = %s',(id,))
        li = cur.fetchone()
        if li:
            return self.convertUserToDict(li)
        else:
            return None

    def findLaboralInsertionCV(self,con,id):
        cur = con.cursor()
        cur.execute('select id,name,cv from laboral_insertion.users_cv where id = %s',(id,))
        li = cur.fetchone()
        if li:
            laboralInsertion = {
                'id':li[0],
                'name':li[1],
                'cv':li[2]
            }
            return laboralInsertion
        else:
            return None


    def persistLaboralInsertion(self,con,data):
        if (self.findLaboralInsertion(con,data['id'])) == None:
            params = (data['id'],data['reside'],data['travel'])
            cur = con.cursor()
            cur.execute("insert into laboral_insertion.users (id,reside,travel) values (%s,%s,%s)",params)
        else:
            params = (data['reside'],data['travel'],data['id'])
            cur = con.cursor()
            cur.execute('update laboral_insertion.users set reside = %s,travel = %s where id = %s',params)



    def persistLaboralInsertionCV(self,con,data):
        if (self.findLaboralInsertionCV(con,data['id'])) == None:
            params = (data['id'],psycopg2.Binary(data['cv']),data['name'])
            cur = con.cursor()
            cur.execute("insert into laboral_insertion.users_cv (id,cv,name) values (%s,%s,%s)",params)
        else:
            params = (psycopg2.Binary(data['cv']),data['name'],data['id'])
            cur = con.cursor()
            cur.execute('update laboral_insertion.users_cv set cv = %s, name = %s where id = %s',params)


    def findAllCvs(self,con):
        cur = con.cursor()
        cur.execute('select cv.cv,cv.name,u.name,u.lastname from laboral_insertion.users_cv as cv, profile.users as u where u.id = cv.id')
        if cur.rowcount <= 0:
            return []

        cvs = []
        for c in cur:
            if c[0] is None:
                continue

            cvs.append({
                'cv':c[0],
                'name':c[1],
                'username':c[2],
                'lastname':c[3]
            })

        return cvs


    def findAll(self,con):
        cur = con.cursor()
        cur.execute('select id,reside,travel,creation from laboral_insertion.users')
        data = cur.fetchall()
        laboralInsertions = []
        for li in data:
            laboralInsertion = self.convertUserToDict(li)
            laboralInsertions.append(laboralInsertion)
        return laboralInsertions

    def convertUserToDict(self,li):
        laboralInsertion = {
            'id':li[0],
            'reside':li[1],
            'travel':li[2],
            'creation':li[3]
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

    def findLanguage(self,con,id):
        cur = con.cursor()
        cur.execute("select id, user_id, name, level from laboral_insertion.languages  WHERE id = '" + id + "'")
        language = cur.fetchone()
        if language != None:
            return self.convertLanguageToDict(language)
        else:
            return None

    def persistLanguage(self,con,data):
        if self.findLanguage(con,data['id']) == None:
            params = (data['id'],data['user_id'],data['name'],data['level'])
            cur = con.cursor()
            cur.execute('insert into laboral_insertion.languages (id,user_id,name,level) values(%s,%s,%s,%s)',params)
        else:
            params = (data['user_id'],degree['name'],degree['level'],degree['id'])
            cur = con.cursor()
            cur.execute('update laboral_insertion.languages set user_id = %s, name = %s, level = %s where id = %s',params)

    def deleteLanguage(self,con,id):
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.languages where id = %s',(id,))

    def deleteLanguages(self,con,user_id):
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.languages where user_id = %s',(user_id,))

    def listLanguages(self,con,user_id):
        cur = con.cursor()
        cur.execute('select id, user_id, name, level from laboral_insertion.languages where user_id = %s',(user_id,))
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
            'courses':d[3],
            'average1':d[4],
            'average2':d[5],
            'work_type':d[6]
        }
        return degree


    def findDegree(self,con,id):
        cur = con.cursor()
        cur.execute("SELECT id,user_id,name,courses,average1,average2,work_type FROM laboral_insertion.degree WHERE id = '" + id + "'")
        degree = cur.fetchone()
        if degree != None:
            return self.convertDegreeToDict(degree)
        else:
            return None

    def persistDegree(self,con,degree):
        if self.findDegree(con,degree['id']) == None:
            params = (degree['id'],degree['user_id'],degree['name'],degree['courses'],degree['average1'],degree['average2'],degree['work_type'])
            cur = con.cursor()
            cur.execute('insert into laboral_insertion.degree (id,user_id,name,courses,average1,average2,work_type) values(%s,%s,%s,%s,%s,%s,%s)',params)
        else:
            params = (degree['user_id'],degree['name'],degree['courses'],degree['average1'],degree['average2'],degree['work_type'],degree['id'])
            cur = con.cursor()
            cur.execute('update laboral_insertion.degree set user_id = %s, name = %s, courses = %s, average1 = %s, average2 = %s, work_type = %s where id = %s',params)


    def deleteDegree(self,con,id):
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.degree where id = %s',(id,))


    def deleteDegrees(self,con,user_id):
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.degree where user_id = %s',(user_id,))

    def listDegrees(self,con,user_id):
        cur = con.cursor()
        cur.execute('select id,user_id,name,courses,average1,average2,work_type from laboral_insertion.degree where user_id = %s',(user_id,))
        data = cur.fetchall()
        degrees = []
        for d in data:
            degrees.append(self.convertDegreeToDict(d))
        return degrees
