# -*- coding: utf-8 -*-
import psycopg2

class Templates:

    def persist(self,con,template):
        cur = con.cursor()
        req = (template['id'],template['template'],template['algorithm'],template['userId'])
        cur.execute('insert into assistance.templates (id,template,algorithm,user_id) values (%s,%s,%s,%s)',req)

    ''' retorna true en el caso de que el template pasado como parámetro tenga una version mayor al de la base '''
    def needSync(self,con,template):
        id = template['id']

        cur = con.cursor()
        cur.execute('select version from assistance.templates where id = %s',(id,))
        cur.rowcount <= 0:
            return True

        version = cur.fetchone()[0]
        return template['version'] > version
