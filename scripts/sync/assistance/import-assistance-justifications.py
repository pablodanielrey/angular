# -*- coding: utf-8 -*-

import csv, sys, pytz, datetime
import psycopg2
from dateutil import parser
import uuid, calendar
import logging
import re


def localice(date):
    if date.tzinfo is not None:
        return date
    timezone = "America/Buenos_Aires"
    tz = pytz.timezone(timezone)
    local = tz.localize(date)
    return local

def replaceTime(date,time):
    return date.replace(hour=time.hour,minute=time.minute,second=0,microsecond=0)



if __name__ == '__main__':


    if len(sys.argv) < 6:
        print('debe invocar el script con los siguientes parámetros :')
        print('cat archivo.csv | python {} host port db user pass'.format(sys.argv[0]))
        sys.exit(1)


    #logging.basicConfig(filename='/tmp/import-schedule.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

    host = sys.argv[1]
    port = sys.argv[2]
    db = sys.argv[3]
    user = sys.argv[4]
    passw = sys.argv[5]



    date = datetime.datetime.now()
    dates = calendar.Calendar().monthdatescalendar(date.year,date.month)
    firstWeek = dates[0][:7]

    con = psycopg2.connect(host=host, port=port, user=user, password=passw, dbname=db)
    cur = con.cursor()
    cur.execute("set time zone %s",('utc',))

    #cur.execute('delete from assistance.schedule')

    logging.basicConfig(level=logging.DEBUG)

    title = False

    try:

        for line in csv.reader(sys.stdin):

            if not title:
                title = True
                continue

            logging.debug(line)

            jp,sfecha,dni,nombre,app,just,hi,hf = line


            #para eliminar el header que siempre queda
            if nombre == 'Nombre':
                continue

            if dni == None or dni == '':
                logging.warn('ignorando {} ya que no tiene dni'.format(line))
                continue


            fecha = parser.parse(sfecha)
            ffecha = fecha.date()

            pid = str(uuid.uuid4())
            cur.execute('select id,dni from profile.users where dni = %s', (dni,))
            if cur.rowcount <= 0:
                cur.execute('insert into profile.users (id,dni,name,lastname) values (%s,%s,%s,%s)', (pid,dni,nombre,app))
            else:
                pid = cur.fetchone()[0]
                cur.execute('update profile.users set name = %s, lastname = %s where id = %s',(nombre,app,pid))
                logging.warn("{0} ya existe - {1}".format(dni,pid))


            """ actualizo para asignarle el perfil de usuario dentro del sistema de asistencia """

            cur.execute('select user_id from credentials.auth_profile where user_id = %s and profile = %s',(pid,'USER-ASSISTANCE'))
            if cur.rowcount <= 0:
                cur.execute('insert into credentials.auth_profile (user_id,profile) values (%s,%s)',(pid,'USER-ASSISTANCE'))


            """ busco la justificacion """

            cur.execute('select id,name from assistance.justifications where name = %s',(just,))
            if cur.rowcount != 1:
                logging.warn('fecha {} ignorando {} ya que no se encuentra la justificacion {}'.format(fecha,dni,just))
                continue


            jId = cur.fetchone()[0]
            if jId == 'fa64fdbd-31b0-42ab-af83-818b3cbecf46':
                logging.warn('No se procesan todavía las boletas de salida')
                continue


            cur.execute('select id from assistance.justifications_requests where jbegin::date = %s',(ffecha,))
            if cur.rowcount > 0:
                logging.warn('{} ya tiene un pedido de justificatión para la fecha {}'.format(dni,fecha))
                continue

            fid = str(uuid.uuid4())
            cur.execute('insert into assistance.justifications_requests (id,user_id,justification_id,jbegin) values (%s,%s,%s,%s)',(fid,pid,jId,fecha))
            cur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status) values (%s,%s,%s)',(fid,pid,'PENDING'))
            cur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status) values (%s,%s,%s)',(fid,'1','APPROVED'))

            con.commit()

    except Exception as e:
        logging.exception(e)



    con.close()
