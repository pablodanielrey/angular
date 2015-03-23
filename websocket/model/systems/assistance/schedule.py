# -*- coding: utf-8 -*-
import psycopg2

class Schedule:

    """
        obtiene tods los schedules para un usuario en determinada fecha, solo deja los actuales, tiene en cuenta el historial ordenado por date
        la fecha esta en UTC
    """
    def getSchedule(self,con,userId,date):

        cur = con.cursor()

        """ obtengo todos los schedules que son en la fecha date del parámetro """
        cur.execute("select sstart, send, date from assistance.schedule where \
                    ((date = %s) or \
                    (isDayOfWeek = true and extract(dow from date) = extract(dow from %s)) or \
                    (isDayOfMonth = true and extract(dom from date) = extract(dom from %s)) or \
                    (isDayOfYear = true and extract(doy from date) = extract(doy from %s))) and \
                    user_id = %s \
                    order by date desc",(date,date,date,date,userId))
        scheduless = cur.fetchall()
        schedules = []
        dateS = None
        for schedule in scheduless:

            """ solo tengo en cuenta los de la ultima fecha """
            dateS = schedule[2] if dateS == None else dateS
            if schedule[2] == dateS:
                schedules.append({'start':schedule[0], 'end':schedule[1]})
            else:
                break

        return schedules


    """
        chequea los logs contra lo que el usuario debería tener ese día
    """
    def checkSchedule(self,con,userId,logs):

        fails = []

        for log in logs:
            start = log['start']
            end = log['end']
            date = start.date()
            schedules = self.getSchedule(con,userId,date)
            if start > schedules[0]['start']:
                fails.append({'schedule_start':,})
