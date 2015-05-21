# -*- coding: utf-8 -*-
import psycopg2

class Templates:

    def persist(self,con,template):
        cur = con.cursor()
        req = (template['id'],template['template'],template['algorithm'],template['userId'])
        cur.execute('insert into assistance.templates (id,template,algorithm,user_id) values (%s,%s,%s,%s)',req)
