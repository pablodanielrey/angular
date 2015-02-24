import psycopg2

class LaboralInsertion:

    def createLaboralInsertion(self,con,student):
        params = ()
        cur = con.cursor()
        cur.execute("insert into laboralInsertion () values (%s,%s)",params)

    def findLaboralInsertion(self,con,id):
        cur = con.cursor()
        cur.execute('select * from laboralInsertion where id = %s',(id))
        li = cur.fetchone()
        if li:
            return self.convertToDic(s)
        else:
            return None

    def findAll(self,con):
        cur = con.cursor()
        cur.execute('select * from laboralInsertion where id = %s',(id))
        li = cur.fetchall()
