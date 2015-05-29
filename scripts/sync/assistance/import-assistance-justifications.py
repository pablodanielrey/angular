# -*- coding: utf-8 -*-

import csv, sys, pytz, datetime
import psycopg2
from dateutil import parser
import uuid, calendar
import logging
import re
import time


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
    dates = calendar.Calendar().monthdatescalendar(date.year,1)
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

            sfecha,dni,just = line


            #para eliminar el header que siempre queda
            if sfecha == 'Fecha':
                continue

            if dni == None or dni == '':
                logging.warn('ignorando {} ya que no tiene dni'.format(line))
                continue


            fecha = datetime.datetime.strptime(sfecha,'%d/%m/%y')

            import pytz, datetime
            local = pytz.timezone ("America/Buenos_Aires")
            local_dt = local.localize(fecha, is_dst=None)
            ffecha = local_dt.astimezone(pytz.utc)


            pid = str(uuid.uuid4())
            cur.execute('select id,dni from profile.users where dni = %s', (dni,))
            if cur.rowcount <= 0:
                cur.execute('insert into profile.users (id,dni,name,lastname) values (%s,%s,%s,%s)', (pid,dni,nombre,app))
            else:
                pid = cur.fetchone()[0]
            """
                cur.execute('update profile.users set name = %s, lastname = %s where id = %s',(nombre,app,pid))
                logging.warn("{0} ya existe - {1}".format(dni,pid))
            """

            """ actualizo para asignarle el perfil de usuario dentro del sistema de asistencia """

            cur.execute('select user_id from credentials.auth_profile where user_id = %s and profile = %s',(pid,'USER-ASSISTANCE'))
            if cur.rowcount <= 0:
                cur.execute('insert into credentials.auth_profile (user_id,profile) values (%s,%s)',(pid,'USER-ASSISTANCE'))


            """ busco la justificacion """

            cur.execute('select id,name from assistance.justifications where lower(name) = lower(%s)',(just,))
            if cur.rowcount != 1:
                logging.warn('\n\n\nFECHA {} ignorando {} ya que no se encuentra la justificacion {}\n\n\n'.format(fecha,dni,just))
                continue


            jId = cur.fetchone()[0]
            """
            if jId == 'fa64fdbd-31b0-42ab-af83-818b3cbecf46':
                logging.warn('No se procesan todavía las boletas de salida')
                continue
            """

            logging.debug('select id from assistance.justifications_requests where jbegin = {} and user_id = {}'.format(ffecha,pid))
            cur.execute('select id from assistance.justifications_requests where jbegin = %s and user_id = %s',(ffecha,pid))
            if cur.rowcount > 0:
                jid = cur.fetchone()[0]
                """
                cur.execute('delete from assistance.justifications_requests_status where request_id = %s',(jid,))
                cur.execute('delete from assistance.justifications_requests where id = %s',(jid,))
                """
                logging.warn('\n\n\n{} YA TIENE PEDIDO de justificatión para la fecha {}, id {}\n\n\n'.format(dni,fecha,jid))
                continue


            logging.warn('insertando {}'.format(line))

            ffecha2 = datetime.datetime.now()
            ffecha3 = ffecha2 + datetime.timedelta(seconds=5)

            fid = str(uuid.uuid4())
            if jId == 'fa64fdbd-31b0-42ab-af83-818b3cbecf46':
                """ boleta de salida - se piden las 3 horas completas desde la segunda marcación que tiene para ese día """

                cur.execute('select log from assistance.attlog where user_id = %s and log::date = %s::date order by log asc',(pid,ffecha))
                if cur.rowcount < 0:
                    logging.warn('\n\nERROR no tiene marcaciones para calcular boleta de salida {} - {}\n\n'.format(pid,ffecha))
                    continue
                logs = cur.fetchall()
                if len(logs) < 2:
                    logging.warn('\n\nERROR no tiene cantidad de marcaciones para calcular boleta de salida {} - {}\n\n'.format(pid,ffecha))
                    continue

                ffecha = logs[1][0]
                efecha = ffecha + datetime.timedelta(hours=3)
                logging.debug('insert into assistance.justifications_requests (id,user_id,justification_id,jbegin,jend,requestor_id) values ({},{},{},{},{},{})'.format(fid,pid,jId,ffecha,efecha,'1'))
                cur.execute('insert into assistance.justifications_requests (id,user_id,justification_id,jbegin,jend,requestor_id) values (%s,%s,%s,%s,%s,%s)',(fid,pid,jId,ffecha,efecha,'1'))
            else:
                logging.debug('insert into assistance.justifications_requests (id,user_id,justification_id,jbegin,requestor_id) values ({},{},{},{},{})'.format(fid,pid,jId,ffecha,'1'))
                cur.execute('insert into assistance.justifications_requests (id,user_id,justification_id,jbegin,requestor_id) values (%s,%s,%s,%s,%s)',(fid,pid,jId,ffecha,'1'))

            logging.debug('insert into assistance.justifications_requests_status (request_id,user_id,status,created) values ({},{},{},{})'.format(fid,pid,'PENDING',ffecha2))
            cur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status,created) values (%s,%s,%s,%s)',(fid,pid,'PENDING',ffecha2))

            logging.debug('insert into assistance.justifications_requests_status (request_id,user_id,status,created) values ({},{},{},{})'.format(fid,'1','APPROVED',ffecha3))
            cur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status,created) values (%s,%s,%s,%s)',(fid,'1','APPROVED',ffecha3))

            """con.commit()"""

    except Exception as e:
        logging.exception(e)


    con.rollback()
    con.close()
