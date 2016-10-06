"""
    Implementa el módulo de estadísticas diarias.

    Métodos para usar el módulo :

        WpStatistics.persist()
        WpStatistics.findByUserId()
        WpStatistics.updateStatistics()

    Para crear estadísticas a partir de un conjunto de WorkedPeriod

        stats = WpStatistics(userId)
        for wp in wpss:
            stats.updateStatistics(wp)

    Para almacenar las estadísticas en la base para generar una cache :

        stats.persist(con)

    Para crear las estadísticas a partir del cache de la base de datos :

        stats = WpStatistics.findByUserId(con, userId, start, end)


"""
from model.users.users import UserDAO
from model.assistance.boss import Boss, BossDAO
from model.serializer import JSONSerializable

from dateutil.tz import tzlocal

class JustificationStatistics(JSONSerializable):

    @staticmethod
    def _create(wp):
        assert wp is not None
        if len(wp.getJustifications()) <= 0:
            return None

        j = JustificationStatistics()
        for js in wp.getJustifications():
            j.identifier = js.getIdentifier()
            j.seconds = js.getJustifiedSeconds(wp)
            j.status = js.getStatus().status
        return j

class DailyWpStatistics(JSONSerializable):
    """ estadisticas diarias """

    @staticmethod
    def _create(con, wp, stats):
        assert wp is not None
        ds = DailyWpStatistics()
        ds.userId = wp.userId
        ds.date = wp.date
        if wp.date is not None:
            bs = Boss.findByUserId(con, [ds.userId], ds.date)
            if len(bs) <= 0:
                ds.isBoss = false
            else:
                ds.isBoss = bs[0].isBoss
        ds.start = wp.getStartDate()
        ds.end = wp.getEndDate()
        ds.iin = None if wp.getStartLog() is None else wp.getStartLog().log.astimezone(tzlocal()).replace(tzinfo=None)
        ds.out = None if wp.getEndLog() is None else wp.getEndLog().log.astimezone(tzlocal()).replace(tzinfo=None)
        ds.justification = JustificationStatistics._create(wp)
        ds._calculatePeriodSeconds(wp, stats)
        ds._caculateWorkedSeconds(wp, stats)
        ds._calculateLateAndEarly(wp, stats)
        ds._calculateAbsence(wp)
        stats._addDailyStatistics(ds)

    def _loadOntoStats(self, stats):
        stats._addToWorkSeconds(self.periodSeconds)
        stats._addWorkedSeconds(self.workedSeconds)
        stats._addSecondsLate(self.lateSeconds)
        stats._addSecondsEarly(self.earlySeconds)
        stats._addDailyStatistics(self)

    def _calculateAbsence(self, wp):
        self.absence = wp.isAbsence()
        self.justificatedAbsence = wp.isJustificatedAbsence()

    def _calculatePeriodSeconds(self, wp, stats):
        self.periodSeconds = wp.getScheduleSeconds()
        stats._addToWorkSeconds(self.periodSeconds)

    def _caculateWorkedSeconds(self, wp, stats):
        self.workedSeconds = wp.getWorkedSeconds()
        stats._addWorkedSeconds(self.workedSeconds)

    def _calculateLateAndEarly(self, wp, stats):
        self.lateSeconds = wp.getLateSeconds()
        if self.lateSeconds > 0:
            stats._addSecondsLate(self.lateSeconds)

        self.earlySeconds = wp.getEarlySeconds()
        if self.earlySeconds > 0:
            stats._addSecondsEarly(self.earlySeconds)

    def isAbsence(self):
        return self.absence

    def isJustificatedAbsence(self):
        return self.justificatedAbsence

    def __init__(self):
        self.userId = None
        self.date = None
        self.start = None
        self.end = None
        self.periodSeconds = 0
        self.iin = None
        self.out = None
        self.workedSeconds = 0
        self.lateSeconds = 0
        self.earlySeconds = 0
        self.absence = False
        self.justificatedAbsence = False
        self.isBoss = False

class WpStatistics(JSONSerializable):

    def __init__(self):
        self.userId = None
        self.position = None                # cargo que ocupa en la facultad
        self.secondsToWork = 0              # total que deberia trabajar
        self.secondsWorked = 0              # total trabajado
        self.secondsLate = 0                # total de llegadas tarde
        self.countLate = 0                  # cantidad de llegadas tarde
        self.secondsEarly = 0               # total de salidas tempranas
        self.countEarly = 0                 # cantidad de salidas tempranas
        self.countAbsences = 0              # cantidad de ausencias
        self.countJustificatedAbsences = 0  # cantidad de ausencias justificadas
        self.dailyStats = []                # estadísticas diarias

    def _addWorkedSeconds(self, s):
        self.secondsWorked = self.secondsWorked + s

    def _addToWorkSeconds(self, s):
        self.secondsToWork = self.secondsToWork + s

    def _addSecondsLate(self, s):
        self.secondsLate = self.secondsLate + s
        self.countLate = self.countLate + 1

    def _addSecondsEarly(self, s):
        self.secondsEarly = self.secondsEarly + s
        self.countEarly = self.countEarly + 1

    def _addDailyStatistics(self, ds):
        if ds.isAbsence():
            self.countAbsences = self.countAbsences + 1
        if ds.isJustificatedAbsence():
            self.countJustificatedAbsences = self.countJustificatedAbsences + 1

        self.dailyStats.append(ds)

    def getStartDate(self):
        return self.dailyStats[0].date

    def getEndDate(self):
        return self.dailyStats[-1].date

    def updateStatistics(self, con, wp):
        assert self.userId == wp.userId
        DailyWpStatistics._create(con, wp, self)

    def persist(self, con):
        WpStatisticsDAO.persist(con, self)

    @staticmethod
    def findByUserId(con, userId, start, end):
        return WpStatisticsDAO.findByUserId(con, userId, start, end)



class WpStatisticsDAO:

    dependencies = [UserDAO, BossDAO]

    @classmethod
    def _createSchema(cls, con):
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;
                create table IF NOT EXISTS assistance.wp_daily_statistics (
                    user_id varchar not null references profile.users (id),
                    sdate date not null,
                    sstart timestamp,
                    send timestamp,
                    sin timestamp,
                    sout timestamp,
                    work bigint default 0,
                    worked bigint default 0,
                    late bigint default 0,
                    early bigint default 0,
                    created timestamptz default now(),
                    unique (user_id, sdate)
                );
            """)
        finally:
            cur.close()

    @staticmethod
    def _dailyFromResult(r):
        ds = DailyWpStatistics()
        ds.userId = r['user_id']
        ds.date = r['sdate']
        ds.start = r['sstart']
        ds.end = r['send']
        ds.periodSeconds = r['work']
        ds.iin = r['sin']
        ds.out = r['sout']
        ds.workedSeconds = r['worked']
        ds.lateSeconds = r['late']
        ds.earlySeconds = r['early']
        return ds

    @staticmethod
    def _findDailyByUserId(con, userId, start, end):
        cur = con.cursor()
        try:
            cur.execute('select * from assistance.wp_daily_statistics where user_id = %s and sdate <= %s and sdate >= %s', (userId, end, start))
            return [ WpStatisticsDAO._dailyFromResult(c) for c in cur ]

        finally:
            cur.close()

    @staticmethod
    def findByUserId(con, userId, start, end):
        dss = WpStatisticsDAO._findDailyByUserId(con, userId, start, end)
        stats = WpStatistics(userId)
        for ds in dss:
            ds._loadOntoStats(stats)
        return stats

    @staticmethod
    def persist(con, stats):
        cur = con.cursor()
        try:
            for ds in stats.dailyStats:
                cur.execute('delete from assistance.wp_daily_statistics where user_id = %s and sdate = %s', (ds.userId, ds.date))
                cur.execute('insert into assistance.wp_daily_statistics (user_id, sdate, sstart, send, work, sin, sout, worked, late, early)'
                            'values (%(userId)s, %(date)s, %(start)s, %(end)s, %(periodSeconds)s, %(iin)s, %(out)s, %(workedSeconds)s, %(lateSeconds)s, %(earlySeconds)s)', ds.__dict__)
        finally:
            cur.close()
