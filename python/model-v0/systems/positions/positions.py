# -*- coding: utf-8 -*-
import uuid
import psycopg2


class Positions:


    def find(self, con, userId):
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


    '''
        actualizar el stock actual para la justificación indicada
    '''
    def update(self,con,userId,position):
        cur = con.cursor()
        cur.execute('''
          SELECT id
          FROM assistance.positions
          WHERE user_id = %s;
        ''',(userId,))


        if cur.rowcount <= 0 and position != None:
            id = str(uuid.uuid4())
            cur.execute('''
                INSERT INTO assistance.positions (id, user_id, name)
                VALUES (%s,%s,%s)
            ''',(id, userId,position))
        else:
            c = cur.fetchone()
            id = c[0];

            if position != None:
                cur.execute('''
                    UPDATE assistance.positions
                    SET user_id = %s, name = %s
                    WHERE id = %s
                ''',(userId,position,id))
            else:
                cur.execute('''
                    DELETE FROM assistance.positions
                    WHERE id = %s
                ''',(id,))

        events = []
        e = {
          'type':'PositionsUpdatedEvent',
          'data':{
             'position':position,
             'userId':userId,
           }
        }
        events.append(e)

        return events
