# -*- coding: utf-8 -*-

import psycopg2

class Positions:


    def find(self,con,userId):
        cur = con.cursor()
        cur.execute('select id,user_id,name from assistance.positions where user_id = %s',(userId,))
        positions = []
        for c in cur:
            positions.append(
                {
                    'id':c[0],
                    'userId':c[1],
                    'name':c[2]
                }
            )
        return positions
