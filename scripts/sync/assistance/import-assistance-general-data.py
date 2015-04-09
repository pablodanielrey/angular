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


def insertOfficeIfNotExist(cur,of,idParent):
    cur.execute('select id from assistance.offices where name = %s',(of,))
    idof = str(uuid.uuid4())
    if cur.rowcount <= 0:
        cur.execute('insert into assistance.offices (id,name,parent) values (%s,%s,%s)',(idof,of,idParent))
    else:
        idof = cur.fetchone()[0]
    return idof


if __name__ == '__main__':


    if len(sys.argv) < 6:
        print('debe invocar el script con los siguientes parámetros :')
        print('cat archivo.csv | python {} host port db user pass'.format(sys.argv[0]))
        sys.exit(1)


    logging.basicConfig(filename='/tmp/import-data.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

    host = sys.argv[1]
    port = sys.argv[2]
    db = sys.argv[3]
    user = sys.argv[4]
    passw = sys.argv[5]



    date = datetime.datetime.now()
    dates = calendar.Calendar().monthdatescalendar(date.year,date.month)
    firstWeek = dates[0][:5]

    con = psycopg2.connect(host=host, port=port, user=user, password=passw, dbname=db)
    cur = con.cursor()
    cur.execute("set time zone %s",('utc',))

    cur.execute('delete from assistance.schedule')
    cur.execute('delete from assistance.positions')
    cur.execute('delete from assistance.offices_users')
    cur.execute('delete from assistance.offices_roles')
    cur.execute('delete from assistance.offices')
    #cur.execute('delete from assistance.justifications_stock')

    logging.basicConfig(level=logging.DEBUG)

    for line in csv.reader(sys.stdin):

        try:
            logging.debug(line)

            nombre,app,func,dni,maili,e,s,of,cargo,ma = line
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


            """ agrego el mail institucional """
            if maili != '':
                cur.execute('select id from profile.mails where email = %s',(maili,))
                if cur.rowcount <= 0:
                    mid = str(uuid.uuid4())
                    cur.execute('insert into profile.mails (id,user_id,email,confirmed,hash) values (%s,%s,%s,%s,%s)',(mid,pid,maili,True,''))

            """ agrego el mail alternativo """
            if ma != '':
                cur.execute('select id from profile.mails where email = %s',(ma,))
                if cur.rowcount <= 0:
                    mid = str(uuid.uuid4())
                    cur.execute('insert into profile.mails (id,user_id,email,confirmed,hash) values (%s,%s,%s,%s,%s)',(mid,pid,ma,False,''))


            """ actualizo las credenciales """

            cur.execute('select id from credentials.user_password where user_id = %s',(pid,))
            if cur.rowcount <= 0:
                logging.debug('Insertando credenciales para el usuario {}'.format(dni))
                cur.execute('insert into credentials.user_password (id,user_id,username,password) values (%s,%s,%s,%s)',(str(uuid.uuid4()),pid,dni,'27294557'))

            """ actualizo para asignarle el perfil de usuario dentro del sistema de asistencia """

            cur.execute('select user_id from credentials.auth_profile where user_id = %s and profile = %s',(pid,'USER-ASSISTANCE'))
            if cur.rowcount <= 0:
                cur.execute('insert into credentials.auth_profile (user_id,profile) values (%s,%s)',(pid,'USER-ASSISTANCE'))


            """ actualizo el tema del horario """

            if e.strip() != '' and s.strip() != '':

                timeE = datetime.datetime.strptime(e,'%H:%M')
                timeS = datetime.datetime.strptime(s,'%H:%M')


                for date in firstWeek:
                    date = datetime.datetime.combine(date,datetime.time())
                    print(date)

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



            """ actualizo los cargos """

            if cargo.strip() != '':
                cur.execute('select id from assistance.positions where user_id = %s',(pid,))
                if cur.rowcount > 0:
                    ppid = cur.fetchone()[0]
                    cur.execute('update assistance.positions set name = %s where id = %s',(cargo,ppid))
                else:
                    req = (str(uuid.uuid4()),pid,cargo)
                    cur.execute('insert into assistance.positions (id,user_id,name) values (%s,%s,%s)',req)



            """ actualizo las oficinas """
            logging.debug('Actualizando la oficina : {}'.format(of))
            r = re.compile('(.*?)\/(.*)')
            p = r.match(of)
            idof = None
            if p:
                off1 = p.group(1)
                off2 = p.group(2)

                logging.debug('insertando oficina {}'.format(off1))
                idoff1 = insertOfficeIfNotExist(cur,off1,None)

                logging.debug('insertando oficina {}'.format(off2))
                idof = insertOfficeIfNotExist(cur,off2,idoff1)
            else:
                logging.debug('insertando oficina {}'.format(of))
                idof = insertOfficeIfNotExist(cur,of,None)

            cur.execute('insert into assistance.offices_users (user_id,office_id) values (%s,%s)',(pid,idof))

            if func != '':
                cur.execute('insert into assistance.offices_roles (user_id,office_id,role) values (%s,%s,%s)',(pid,idof,'autoriza'))


            con.commit()

        except Exception as e:
            logging.debug(e)



    con.close()
