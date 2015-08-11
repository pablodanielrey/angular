# -*- coding: utf-8 -*-
import psycopg2

class Templates:

    def persist(self,con,template):
        cur = con.cursor()
        req = (template['id'],template['template'],template['algorithm'],template['userId'],template['version'])
        cur.execute('insert into assistance.templates (id,template,algorithm,user_id,version) values (%s,%s,%s,%s,%s)',req)

    def update(self,con,template):
        cur = con.cursor()
        cur.execute('select id from assistance.templates where id = %s',(template['id'],))
        if cur.rowcount <= 0:
            self.persist(con,template)
        else:
            req = (template['template'],template['algorithm'],template['userId'],template['version'],template['id'])
            cur.execute('update assistance.templates set template = %s, algorithm = %s, user_id = %s, version where id = %s values (%s,%s,%s,%s,%s)',req)


    def findByUser(self,con,userId):
        cur = con.cursor()
        cur.execute('select id,template,algorithm,user_id,version from assistance.templates where user_id = %s',(userId,))
        if cur.rowcount <= 0:
            return []

        templates = []
        for t in cur:
            temp = self._fromDict(t)
            templates.append(temp)

        return templates


    def _fromDict(self,t):
        template = {
            'id':t[0],
            'template':t[1],
            'algorithm':t[2],
            'userId':t[3],
            'version':t[4]
        }
        return template

    ''' retorna true en el caso de que el template pasado como parámetro tenga una version mayor al de la base '''
    def needSync(self,con,template):
        id = template['id']

        cur = con.cursor()
        cur.execute('select version from assistance.templates where id = %s',(id,))
        if cur.rowcount <= 0:
            return True

        version = cur.fetchone()[0]
        return template['version'] > version
