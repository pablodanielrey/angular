import psycopg2
from model.objectView import ObjectView

class LaboralInsertions:

    def createLaboralInsertion(self,con,laboralInsertion):
        params = (laboralInsertion['id'],laboralInsertion['cv'],laboralInsertion['residir'],laboralInsertion['viajar'])
        cur = con.cursor()
        cur.execute("insert into laboral_insertion.users (id,cv,reside,travel) values (%s,%s,%s,%s)",params)

    def updateLaboralInsertion(self,con,li):
        laboralInsertion = ObjectView(li)
        params = (laboralInsertion.cv,laboralInsertion.residir,laboralInsertion.viajar,laboralInsertion.id)
        cur = con.cursor()
        cur.execute('update laboral_insertion.users set cv = %s,reside = %s,travel = %s where id = %s',params)

    def findLaboralInsertion(self,con,id):
        cur = con.cursor()
        cur.execute('select id,cv,reside,travel from laboral_insertion.users where id = %s',(id))
        li = cur.fetchone()
        if li:
            return self.convertToDic(s)
        else:
            return None

    def findAll(self,con):
        cur = con.cursor()
        cur.execute('select id,cv,reside,travel from laboral_insertion.users where id = %s',(id))
        data = cur.fetchall()
        laboralInsertions = []
        for li in data:
            laboralInsertion = self.convertToDict(li)
            laboralInsertions.append(laboralInsertion)
        return laboralInsertions

    def convertToDict(self,li):
        laboralInsertion = {
            'id':li[0],
            'cv':li[1],
            'reside':li[2],
            'travel':li[3]
        }
        return laboralInsertion
