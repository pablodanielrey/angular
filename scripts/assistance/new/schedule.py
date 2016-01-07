import psycopg2
import logging
import datetime
import json

logging.getLogger().setLevel(logging.INFO)


def getConnection():
    con = psycopg2.connect(host='163.10.17.80', database='dcsys', user='dcsys', password='dcsys')
    return con


class ScheduleModel:
    ''' modelo del sistema que encapsula el manejo de schedules '''

    def findSchedulesFor(userId, start, end):
        ''' obtiene los schedules del usuario entre determinadas fechas '''


class WorkedHours:
    ''' franja de horarios '''

    def __init__(self, start, end):
        self.start = start
        self.end = end


class ScheduleData:
    ''' schedule que representa un período laboral y sus horarios dentro de ese período '''
    __serializable__ = True

    def __init__(self):
        self.ids = []
        self.dates = []
        self.workedHours = []


class Schedule:
    ''' schedule como esta representado en la base de datos. '''

    def __init__(self):
        self.id = ''
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

    def _fromSchedule(self, date, schedules):
        ''' retorna un scheduleData a partir de una lista de schedules que representan el mismo período laboral con horario cortado '''
        sd = ScheduleData()

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
        return s

    def _findAllBetween(self, con, userId, start, end):
        ''' retorna todos los ScheduleData que representan los períodos laborales entre start (inclusive) y end (inclusive) '''
        cur = con.cursor()
        try:

            scheduleDatas = []
            specificDates = []

            cur.execute("select sdate, sstart, send, isDayOfWeek, isDayOfMonth, isDayOfYear, id from assistance.schedule where sdate <= %s and user_id = %s order by sdate desc", (end, userId))
            schedulesCur = cur.fetchall()
            schedules = [Schedule._fromMap(s) for s in schedulesCur]

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
                    scheduleData = self._fromSchedule(sdate, sameDay)
                    scheduleDatas.append(scheduleData)

            if len(wheekly) > 0:
                ''' se calculan los horarios semanales '''
                actual = start
                while actual <= end:
                    if actual in specificDates:
                        ''' si ya es una fecha calculada especificamente se toma esa como primaria y no se tiene en cuenta el horario semanal '''
                        actual = actual + datetime.timedelta(days=1)
                        continue

                    wd = actual.weekday()
                    daySchedules = [s for s in wheekly if s.date.weekday() == wd and s.date <= actual]
                    if len(daySchedules) <= 0:
                        actual = actual + datetime.timedelta(days=1)
                        continue

                    assert len(daySchedules) > 0
                    lastDaySchedules = [s for s in daySchedules if s.date == daySchedules[0].date]
                    scheduleData = self._fromSchedule(actual, lastDaySchedules)
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
    s = Schedule()

    cur = con.cursor()
    cur.execute('select distinct user_id from assistance.schedule')
    users = cur.fetchall()
    for u in users:
        uid = u[0]
        logging.info('\n----------{}-----------\n'.format(uid))
        scheds = s._findAllBetween(con, uid, datetime.datetime(2012, 12, 1), datetime.datetime(2016, 12, 1))
        logging.info(scheds)
        logging.info(len(scheds))

        ss = Serializer.dumps(scheds)
        ss2 = Serializer.loads(ss)

        """
        for s2 in scheds:
            logging.info('dates: {}'.format(s2.dates))
            for wh in s2.workedHours:
                logging.info('wh {} -> {}'.format(wh.start, wh.end))
            logging.info('\n')
            if len(s2.workedHours) > 1:
                logging.info('parando')
                break
        """
