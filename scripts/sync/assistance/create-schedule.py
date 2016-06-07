# -*- coding: utf-8 -*-

import uuid,sys,datetime,pytz
import dateutil, dateutil.tz
import psycopg2


if __name__ == '__main__':
  dbhost = sys.argv[1]
  dbname = sys.argv[2]
  dbuser = sys.argv[3]
  dbpass = sys.argv[4]

  dni = sys.argv[5]
  #date = datetime.datetime(2015, 10, 8, 0, 0, 0)
  #start = datetime.datetime(2015, 10, 8, 15, 0, 0)
  #end =  datetime.datetime(2015, 10, 8, 19, 0, 0)
  date = datetime.datetime(2015, 10, 10, 0, 0, 0)
  start = datetime.datetime(2015, 10, 10, 11, 0, 0)
  end =  datetime.datetime(2015, 10, 10, 15, 0, 0)  
  isDayOfWeek = True
  
  tz = dateutil.tz.tzlocal()
  date = date.replace(tzinfo=tz)
  start = start.replace(tzinfo=tz)
  end = end.replace(tzinfo=tz)  


  


  con = psycopg2.connect(host=dbhost, dbname=dbname, user=dbuser, password=dbpass)

  cur = con.cursor()

  # chequeo de que exista la base de datos
  cur.execute('select id from profile.users where dni = %s', (dni,))
  data = cur.fetchone()
  if data == None:
      print ("el usuario no existe")
      sys.exit(1)
      


  uaware = date.astimezone(pytz.utc)
  ustart = start.astimezone(pytz.utc)
  uend = end.astimezone(pytz.utc)

  cur = con.cursor()
  cur.execute('set time zone %s', ('utc',))


  userId = data[0]
  id = str(uuid.uuid4())
  req = (id, userId, uaware, ustart, uend, isDayOfWeek)
  cur.execute('insert into assistance.schedule (id,user_id,date,sstart,send,isDayOfWeek) values (%s,%s,%s,%s,%s,%s)', req)

  con.commit()
  con.close()