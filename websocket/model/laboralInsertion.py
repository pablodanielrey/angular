import psycopg2
from model.objectView import ObjectView

class LaboralInsertions:

    def createLaboralInsertion(self,con,laboralInsertion):
        params = (laboralInsertion['id'],laboralInsertion['cv'],laboralInsertion['residir'],laboralInsertion['viajar'])
        cur = con.cursor()
        cur.execute("insert into laboralInsertion (id,cv,residir,viajar) values (%s,%s,%s,%s)",params)

    def updateLaboralInsertion(self,con,li):
        laboralInsertion = ObjectView(li)
        params = (laboralInsertion.cv,laboralInsertion.residir,laboralInsertion.viajar,laboralInsertion.id)
        cur = con.cursor()
        cur.execute('update laboralInsertion set cv = %s,residir = %s,viajar = %s where id = %s',params)

    def findLaboralInsertion(self,con,id):
        cur = con.cursor()
        cur.execute('select id,cv,residir,viajar from laboralInsertion where id = %s',(id))
        li = cur.fetchone()
        if li:
            return self.convertToDic(s)
        else:
            return None

    def findAll(self,con):
        cur = con.cursor()
        cur.execute('select id,cv,residir,viajar from laboralInsertion where id = %s',(id))
        data = cur.fetchall()
        laboralInsertions = []
        for li in data:
            laboralInsertion = self.convertToDict(li)
            laboralInsertions.append(laboralInsertion)
        return laboralInsertions

    def convertToDict(self,li) {
        laboralInsertion = {
            'id':li[0],
            'cv':li[1],
            'residir':li[2],
            'viajar':li[3]
        }
        return laboralInsertion
    }
