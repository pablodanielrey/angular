
import uuid
import json
import datetime
import sys
sys.path.append('../../python')

import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection.connection import Connection
from model.assistance.schedules import ScheduleDAO

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    try:
        con = conn.get()

        #ScheduleDAO._createSchema(con)

        cur = con.cursor()
        try:
            cur.execute('select id, user_id, created, sdate, sstart, send from assistance.schedule where isdayofweek = true')
            for c in cur.fetchall():
                params = {
                    'id': c['id'],
                    'userId': c['user_id'],
                    'created': c['created'],
                    'start': c['sstart'],
                    'end': c['send'],
                    'date': c['sdate'],
                    'weekday': c['sdate'].weekday()
                }
                cur.execute('insert into assistance.schedules (id, user_id, created, sdate, sstart, send, weekday) values '
                            '(%(id)s, %(userId)s, %(created)s, %(date)s, %(start)s, %(end)s, %(weekday)s)', params)


            """ ahora genero los dias que son fechas especiales, los genero como cambios de horario de semana """
            cur.execute('select id, user_id, created, sdate, sstart, send from assistance.schedule where isdayofmonth = false and isdayofweek = false and isdayofyear = false')
            for c in cur.fetchall():

                """ guardo el schedule que tenía para esa fecha, asi cambio el horario nuevamente en la fecha del dia siguiente """
                specificDate = c['sdate']
                sa = ScheduleDAO.findByUserIdInDate(con, c['user_id'], specificDate)

                params = {
                    'id': c['id'],
                    'userId': c['user_id'],
                    'created': c['created'],
                    'start': c['sstart'],
                    'end': c['send'],
                    'date': c['sdate'],
                    'weekday': c['sdate'].weekday()
                }
                cur.execute('insert into assistance.schedules (id, user_id, created, sdate, sstart, send, weekday) values '
                            '(%(id)s, %(userId)s, %(created)s, %(date)s, %(start)s, %(end)s, %(weekday)s)', params)


                if sa is not None:
                    """ genero el cambio de horario nuevamente a lo que tenia originalmente enla proxima fecha  """

                    params = {
                        'id': str(uuid.uuid4()),
                        'userId': sa.userId,
                        'created': datetime.datetime.now(),
                        'start': sa.start,
                        'end': sa.end,
                        'date': specificDate + datetime.timedelta(1),
                        'weekday': sa.date.weekday()
                    }
                    cur.execute('insert into assistance.schedules (id, user_id, created, sdate, sstart, send, weekday) values '
                                '(%(id)s, %(userId)s, %(created)s, %(date)s, %(start)s, %(end)s, %(weekday)s)', params)



            con.commit()

        finally:
            cur.close()

    finally:
        conn.put(con)
