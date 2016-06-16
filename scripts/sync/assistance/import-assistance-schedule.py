# -*- coding: utf-8 -*-

import csv, sys, pytz, datetime
import psycopg2
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
    dates = calendar.Calendar().monthdatescalendar(date.year,date.month-1)
    firstWeek = dates[0][:7]

    con = psycopg2.connect(host=host, port=port, user=user, password=passw, dbname=db)
    cur = con.cursor()
    cur.execute("set time zone %s",('utc',))

    #cur.execute('delete from assistance.schedule')

    logging.basicConfig(level=logging.DEBUG)

    lines = 0

    for line in csv.reader(sys.stdin):

        try:
            logging.debug(line)

            """ salto el titulo """
            if lines < 2:
                lines = lines + 1
                continue

            nombre,app,dni,le,ls,me,ms,mme,mms,je,js,ve,vs,se,ss,de,ds = line

            #para eliminar el header que siempre queda
            if nombre == 'Nombre':
                continue

            if dni == None or dni == '':
                logging.warn('ignorando {} ya que no tiene dni'.format(line))
                continue

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


            """ actualizo el tema del horario """

            cur.execute('delete from assistance.schedule where user_id = %s',(pid,))

            entradas = [le,me,mme,je,ve,se,de]
            salidas = [ls,ms,mms,js,vs,ss,ds]
            for i in range(7):
                e = entradas[i]
                s = salidas[i]
                date = firstWeek[i]

                if e.strip() != '' and s.strip() != '':

                    logging.debug('procesando fecha {} entrada {} y salida {}'.format(date,e,s))

                    timeE = datetime.datetime.strptime(e,'%H:%M:%S')
                    timeS = datetime.datetime.strptime(s,'%H:%M:%S')

                    date = datetime.datetime.combine(date,datetime.time())
                    logging.debug('generando schedule para la fecha {}'.format(date))

                    awareDate = localice(date)

                    #awareDate = aware.replace(hour=0,minute=0,second=0,microsecond=0)
                    sstart = replaceTime(awareDate,timeE)
                    send = replaceTime(awareDate,timeS)

                    uaware = awareDate.astimezone(pytz.utc)
                    ustart = sstart.astimezone(pytz.utc)
                    uend = send.astimezone(pytz.utc)

                    req = (str(uuid.uuid4()), pid, uaware, ustart, uend, True, False, False)
                    logging.debug('Insertando schedule : {}'.format(str(req)))
                    cur.execute('insert into assistance.schedule (id,user_id,date,sstart,send,isDayOfWeek,isDayOfMonth,isDayOfYear) values (%s,%s,%s,%s,%s,%s,%s,%s)',req)


            con.commit()

        except Exception as e:
            logging.exception(e)



    con.close()
