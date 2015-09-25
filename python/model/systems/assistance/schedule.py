# -*- coding: utf-8 -*-
import psycopg2
import inject
import uuid
import datetime
import pytz
import calendar
import logging
import pdb

from model.exceptions import *

from model import utils
from model.systems.assistance.date import Date
from model.systems.assistance.logs import Logs


class ScheduleData:
    ''' representa datos del schedule '''

    def __init__(self, s, dateStart = None, dateEnd = None):
        self.id = s['id']
        self.date = s['date']
        self.start = s['start']
        self.end = s['end']
        self.isDayOfWeek = s['isDayOfWeek']
        self.isDayOfMonth = s['isDayOfMonth']
        self.isDayOfYear = s['isDayOfYear']
        
        self.dateStart = dateStart
        self.dateEnd = dateEnd


    def _checkDate(date):

        if self.isDayOfWeek:
            d = datetime.date.weekday(self.date)
            d1 = datetime.date.weekday(date)
            return (d1 == d)

        ''' ... lo mismo con dia del mes y dia del año ... '''

        if (dateStart > date) or (dateEnd > date):
            return False
        return True
    
    def _getStart(self):
        return self.start
    
    
    def getStart(self,date):
        ''' retorna el datetime del inicio del schedule '''

        if not self._checkDate(date):
            return None

        zero = datetime.time(hour=0, minute=0, second=0)
        dzero = datetime.combine(date, zero)
        start = dzero + datetime.timedelta(seconds=self.start)

        return start

    def getEnd(date):
        ''' retorna el datetime del fin del schedule '''

        if not self._checkDate(date):
            return None

        zero = datetime.time(hour=0, minute=0, second=0)
        dzero = datetime.combine(date, zero)
        end = dzero + datetime.timedelta(seconds=self.end)

        return end


class Schedule:

    logs = inject.attr(Logs)
    date = inject.attr(Date)


    """
        Retorna la lista de logs determinada que deberia tener un usuario para un schedule,
        se tiene en cuenta el horario de la persona en la fecha y la fecha siguiente para obtener los logs correctos.
        @param schedules Lista de schedules Suponemos que la lista es de la misma fecha a consultar
    """
    def getLogsForSchedule(self, con, userId, schedules):

        if schedules is None:
            return []

        if len(schedules) <= 0:
            return []


        #definir timestamps de inicio y finalizacion
        dateStart = schedules[0].date
        start = schedules[0].getStart(dateStart)
        
        dateEnd = schedules[-1].date
        end = schedules[-1].getEnd(dateEnd)

        deltaEnd = end + datetime.timedelta(hours=3)
        deltaStart = start - datetime.timedelta(hours=3)

        logs = self.logs.findLogs(con, userId, deltaStart, deltaEnd)

        return logs


    """
        obtiene tods los schedules para un usuario en determinada fecha, solo deja los actuales, tiene en cuenta el historial ordenado por date
        la fecha esta en UTC
    """
    def getSchedule(self, con, userId, date):
        cur = con.cursor()
        cur.execute('set time zone %s', ('utc',))

        """ obtengo todos los schedules que son en la fecha date del parámetro """
        cur.execute("select id, sstart, send, sdate, isDayOfWeek, isDayOfMonth, isDayOfYear from assistance.schedule where \
                    ((sdate = %s) or \
                    (isDayOfWeek = true and sdate <= %s and extract(dow from sdate) = extract(dow from %s)) or \
                    (isDayOfMonth = true and sdate <= %s and extract(day from sdate) = extract(day from %s)) or \
                    (isDayOfYear = true and sdate <= %s and extract(doy from sdate) = extract(doy from %s))) and \
                    user_id = %s \
                    order by sdate desc", (date, date, date, date, date, date, date, userId))
       
        scheduless = cur.fetchall()
        if scheduless is None or len(scheduless) <= 0:
            return []

        schedules = []
        for schedule in scheduless:
  
            sch = {
                'id': schedule[0],
                'date': schedule[1],
                'start': schedule[2],
                'end': schedule[3],
                'isDayOfWeek': schedule[4],
                'isDayOfMonth': schedule[5],
                'isDayOfYear': schedule[6]                                   
            }
            
            schData = ScheduleData(sch) 
            
            #retorno los schedules con la fecha actual en utc - las fechas en la base deberian estar en utc
            schedules.append(schData)
                

        # ordeno los schedules por el start
        #schedules = sorted(schedules, key=lambda schedule: schedule.getStart(date))

        return schedules


    """
        obtiene todos los schedules para un usuario
    """
    def getSchedulesHistory(self, con, userId):
        cur = con.cursor()
        cur.execute('set time zone %s', ('utc',))

        cur.execute("select sstart, send, date, isDayOfWeek, isDayOfMonth, isDayOfYear, id from assistance.schedule where \
                user_id = %s \
                order by date desc", (userId,))
        scheduless = cur.fetchall()
        if scheduless is None or len(scheduless) <= 0:
            return []

        schedules = []

        if not self.date.isUTC(scheduless[0][2]):
            raise FailedConstraints('date in database not in UTC')

        for schedule in scheduless:

            """ controlo que las fechas están en utc """
            if not (self.date.isUTC(schedule[0]) and self.date.isUTC(schedule[1])):
                raise FailedConstraints('date in database not in UTC')

            """ retorno los schedules con la fecha actual en utc - las fechas en la base deber�an estar en utc """
            schedules.append(
                {
                    'id': schedule[6],
                    'start': schedule[0],
                    'end': schedule[1],
                    'date': schedule[2],
                    'isDayOfWeek': schedule[3],
                    'isDayOfMonth': schedule[4],
                    'isDayOfYear': schedule[5]
                }
            )

        return schedules

    """
        obtiene los schedules de la semana pasada en el date para un usuario
    """
    def getSchedulesOfWeek(self,con,userId,date):

        if date is None:
            date = self.date.now()
            date = date.replace(hour=0,minute=0,second=0,microsecond=0)

        # paso la fecha a utc
        date = self.date.awareToUtc(date)

        # obtengo el primer dia de la semana del date (L-0 .. D-6)
        weekday = datetime.date.weekday(date)
        date -= datetime.timedelta(days=weekday)

        schedules = []

        for x in range(0, 7):
            sch = self.getSchedule(con,userId,date)
            schedules.append(sch)
            date += datetime.timedelta(days=1)

        return schedules

    """
        reotnra los ids de los usuarios que tiene algun contról de horario
    """
    def getUsersInSchedules(self, con):
        cur = con.cursor()
        cur.execute('select distinct user_id from assistance.schedule')
        if cur.rowcount <= 0:
            return []

        users = []
        for c in cur:
            users.append(c[0])
        return users



    """
        genera un nuevo schedule las fechas pasadas como parámetro (se supone aware)
    """
    def persistSchedule(self, con, userId, date, start, end, isDayOfWeek, isDayOfMonth, isDayOfYear):
        uaware = date.astimezone(pytz.utc)
        ustart = start.astimezone(pytz.utc)
        uend = end.astimezone(pytz.utc)

        cur = con.cursor()
        cur.execute('set time zone %s', ('utc',))

        id = str(uuid.uuid4())
        req = (id, userId, uaware, ustart, uend, isDayOfWeek, isDayOfMonth, isDayOfYear)
        cur.execute('insert into assistance.schedule (id,user_id,date,sstart,send,isDayOfWeek,isDayOfMonth,isDayOfYear) values (%s,%s,%s,%s,%s,%s,%s,%s)', req)
        return id

    '''
        elimina un schedule
    '''
    def deleteSchedule(self, con, id):
        cur = con.cursor()
        cur.execute('delete from assistance.schedule where id = %s', (id,))

    '''
        combina los whs con los schedules
        retorna [{schdule:{},whs:[]}]
    '''
    def combiner(self, schedules, whs):
        controls = []

        if schedules is None or len(schedules) == 0:
            return controls

        # ordeno los schedules y los whs por horario ascendente
        schedules = sorted(schedules, key=lambda schedule: schedule['start'])
        whs = sorted(whs, key=lambda wh: wh['start'])

        for sched in schedules:
            elem = {'schedule':sched,'whs':[]}
            if len(schedules) == 1:
                elem['whs'].extend(whs)
                whsAppends = whs
            else:
                whsAppends = []
                for wh in whs:
                    if 'start' in wh and wh['start'] <= sched['end']:
                        elem['whs'].append(wh)
                        whsAppends.append(wh)

                for w in whsAppends:
                    whs.remove(w)

            controls.append(elem)

        return controls
