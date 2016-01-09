# -*- coding: utf-8 -*-
'''
    Implementa todo el codigo relacionado al modelo y las entidades de los schedules
'''
import psycopg2
from psycopg2 import pool
import logging
import datetime
import json
import redis
import uuid

logging.getLogger().setLevel(logging.INFO)

pool = psycopg2.pool.ThreadedConnectionPool(10, 20, host='163.10.17.80', database='dcsys', user='dcsys', password='dcsys')


def getConnection():
    global pool
    return pool.getconn()


def closeConnection(con):
    global pool
    pool.putconn(con)


class ScheduleModel:
    ''' modelo del sistema que encapsula el manejo de schedules '''

    @staticmethod
    def findAllBetween(userId, start, end):
        ''' obtiene los schedules del usuario entre determinadas fechas '''
        r = redis.StrictRedis(host='163.10.17.21', port=6379)

        cache = []
        dates = []

        actual = start
        while actual <= end:
            scheduleData = ScheduleData._loadFromCache(r, userId, actual)
            if scheduleData:
                cache.append(scheduleData)
                dates.append(actual)
            actual = actual + datetime.timedelta(days=1)

        con = getConnection()
        try:
            scheds = Schedule.findAllBetween(con, userId, start, end, dates)
            for s in scheds:
                s._storeInCache(r)

            scheds.extend(cache)
            scheds = sorted(scheds, key=lambda x: x.dates)

            return scheds

        finally:
            closeConnection(con)


class WorkedHours:
    ''' franja de horarios '''

    def __init__(self, start, end):
        self.start = start
        self.end = end


class ScheduleData:
    ''' schedule que representa un período laboral y sus horarios dentro de ese período '''

    def __init__(self):
        self.userId = ''
        self.ids = []
        self.dates = []
        self.workedHours = []

    def _storeInCache(self, cache):
        ''' almaceno en la cache el scheduleData y tambien genero los indices de las fechas hacia ese schedule '''
        schedIndex = 'ScheduleData_{}_{}'.format(self.userId, ''.join([str(d) for d in self.dates]))
        logging.info('almacenando en cache {}'.format(schedIndex))
        sched = Serializer.dumps(self)
        cache.set(schedIndex, str(sched))
        for date in self.dates:
            sid = 'ScheduleData_{}_{}'.format(self.userId, date)
            logging.info('almacenando en cache {}'.format(sid))
            cache.set(sid, str(schedIndex))

    @staticmethod
    def _loadFromCache(cache, userId, date):
        ''' carga el ScheduleData desde cache y lo retorna o retorna None en caso de no existir '''
        sid = 'ScheduleData_{}_{}'.format(userId, date)
        logging.info('cargando desde cache {}'.format(sid))
        schedIndex = cache.get(sid)
        if schedIndex:
            logging.info('cargando desde cache index {}'.format(schedIndex))
            sched = cache.get(str(schedIndex))
            if sched:
                logging.info('ss {}'.format(sched))
                schedule = Serializer.loads(str(sched))
                return schedule
        return None


class Schedule:
    ''' schedule como esta representado en la base de datos. '''

    def __init__(self):
        self.id = ''
        self.userId = ''
        self.date = datetime.datetime.now()
        self.start = 60 * 60 * 6
        self.end = self.start + (60 * 60 * 7)
        self.version = 0
        self.null = False
        self.user = ''
        self.created = datetime.datetime.now()
        self.isDayOfMonth = False
        self.isDayOfWeek = True
        self.isDayOfYear = False

    @staticmethod
    def _fromMap(map):
        ''' retorna un Schedule a partir del mapa retornado de la consulta a la base '''
        s = Schedule()
        s.date = datetime.datetime.combine(map[0], datetime.time())
        s.start = map[1]
        s.end = map[2]
        s.isDayOfWeek = map[3]
        s.isDayOfMonth = map[4]
        s.isDayOfYear = map[5]
        s.id = map[6]
        s.userId = map[7]
        return s

    @classmethod
    def _fromSchedule(cls, date, schedules):
        ''' retorna un scheduleData a partir de una lista de schedules que representan el mismo período laboral con horario cortado '''
        sd = ScheduleData()
        sd.userId = schedules[0].userId

        ''' calculamos las fechas para las cuales vale este schedule '''
        end = date + datetime.timedelta(seconds=schedules[-1].end)
        while date <= end:
            sd.dates.append(date)
            date = date + datetime.timedelta(days=1)

        for s in schedules:
            assert s.id is not None
            assert s.date is not None
            assert s.start is not None
            assert s.end is not None
            sd.ids.append(s.id)
            start = date + datetime.timedelta(seconds=s.start)
            end = date + datetime.timedelta(seconds=s.end)
            w = WorkedHours(start, end)
            sd.workedHours.append(w)

        return sd

    @classmethod
    def findAllBetween(cls, con, userId, start, end, exceptDates=None):
        ''' retorna todos los ScheduleData que representan los períodos laborales entre start (inclusive) y end (inclusive) '''
        cur = con.cursor()
        try:

            scheduleDatas = []
            specificDates = []

            cur.execute("select sdate, sstart, send, isDayOfWeek, isDayOfMonth, isDayOfYear, id, user_id from assistance.schedule where sdate <= %s and user_id = %s order by sdate desc", (end, userId))
            schedulesCur = cur.fetchall()
            schedules = [cls._fromMap(s) for s in schedulesCur]

            specific = [s for s in schedules if not s.isDayOfMonth and not s.isDayOfWeek and not s.isDayOfYear and s.date >= start]
            wheekly = [s for s in schedules if s.isDayOfWeek]

            logging.info(specific)

            if len(specific) > 0:
                ''' se calculan los horarios específicos '''
                while len(specific) > 0:
                    sdate = specific[0].date
                    specificDates.append(sdate)
                    sameDay = [s for s in specific if s.date == sdate]
                    specific = [s for s in specific if s not in sameDay]
                    if sdate not in exceptDates:
                        scheduleData = cls._fromSchedule(sdate, sameDay)
                        scheduleDatas.append(scheduleData)

            if len(wheekly) > 0:
                ''' se calculan los horarios semanales '''
                actual = start
                while actual <= end:
                    if actual in specificDates:
                        ''' si ya es una fecha calculada especificamente se toma esa como primaria y no se tiene en cuenta el horario semanal '''
                        actual = actual + datetime.timedelta(days=1)
                        continue

                    if actual in exceptDates:
                        ''' una fecha que no se debe calcular ya que fue pasada como parámetro '''
                        actual = actual + datetime.timedelta(days=1)
                        continue

                    wd = actual.weekday()
                    daySchedules = [s for s in wheekly if s.date.weekday() == wd and s.date <= actual]
                    if len(daySchedules) <= 0:
                        actual = actual + datetime.timedelta(days=1)
                        continue

                    assert len(daySchedules) > 0
                    lastDaySchedules = [s for s in daySchedules if s.date == daySchedules[0].date]
                    scheduleData = cls._fromSchedule(actual, lastDaySchedules)
                    scheduleDatas.append(scheduleData)
                    actual = scheduleData.dates[-1] + datetime.timedelta(days=1)

            ''' reordeno la lista por las fechas especificas y las semanas generadas '''
            scheduleDatas = sorted(scheduleDatas, key=lambda x: x.dates)
            return scheduleDatas

        finally:
            cur.close()


if __name__ == '__main__':
    from serializer import Serializer

    con = getConnection()

    cur = con.cursor()
    cur.execute('select distinct user_id from assistance.schedule')
    users = cur.fetchall()
    closeConnection(con)

    for u in users:
        uid = u[0]
        logging.info('\n----------{}-----------\n'.format(uid))
        scheds = ScheduleModel.findAllBetween(uid, datetime.datetime(2016, 11, 1), datetime.datetime(2016, 12, 1))
        break
        """
        logging.info(scheds)
        logging.info(len(scheds))
        for s2 in scheds:
            ss2 = Serializer.dumps(s2)
            logging.info(ss2)
            s2 = Serializer.loads(ss2)
            logging.info('dates: {}'.format(s2.dates))
            for wh in s2.workedHours:
                logging.info('wh {} -> {}'.format(wh.start, wh.end))
            logging.info('\n')
        """
