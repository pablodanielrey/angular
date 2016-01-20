# -*- coding: utf-8 -*-
import signal
import sys
import inject, psycopg2
import logging
import datetime
import pdb

logging.getLogger().setLevel(logging.DEBUG)

# sys.path.append('../python')
sys.path.insert(0, '../../../python')

con = psycopg2.connect(host="163.10.17.80", dbname="dcsys", user="dcsys", password="dcsys")
cur = con.cursor()

begin = datetime.datetime(2015, 2, 1, 0, 0, 0, 0)
end = datetime.datetime(2015, 9, 30, 23, 59, 59, 999999)
elapsed = datetime.timedelta(hours=12)
userId = '5405c989-9dd2-4a4d-929f-a6e9d296748a'

logging.info('realizando consulta')
cur.execute('SELECT * FROM assistance.attlog WHERE user_id = %s AND log > %s AND log < %s', (userId, begin, end))
logging.info('obteniendo resultados')
logs = cur.fetchall()
con.close()


with open('/tmp/horario.csv','w') as f:

    f.write('dia entrada;hora entrada;dia salida;hora salida;cantidad de horas\n')

    logging.info('procesando resultados')
    i = 0
    while i < len(logs):
        s = logs[i][4]

        if i + 1 >= len(logs):
            sys.exit()

        i = i + 1
        e = logs[i][4]
        i = i + 1

        # logging.info('chequeando {} < {}'.format(e,s + elapsed))

        if e < s:
            ''' la salida es menor que la entrada, la ignoro '''
            continue

        hours = e - s
        chours = hours.seconds//3600
        chours = chours + hours.days * 24
        shours = '{}:{}'.format(chours,(hours.seconds//60)%60)

        if e < s + elapsed:
            f.write('{};{};{};{};{}\n'.format(s.date(),s.strftime('%H:%M'),e.date(),e.strftime('%H:%M'),shours))
        else:
            f.write('{};{};{};{};{}\n'.format(s.date(),s.strftime('%H:%M'),e.date(),e.strftime('%H:%M'),shours))
            i = i - 1
