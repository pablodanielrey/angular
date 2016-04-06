
import datetime
from model.serializer.utils import JSONSerializable

class Schedule(JSONSerializable):

    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

    def __init__(self):
        self.userId = None
        self.date = None
        self.weekday = -1
        self.start = None
        self.end = None
        self.daily = False

    def isValid(self, date):
        return (self.date <= date) and (self.weekday == date.weekday())

    def getStartDate(self, date):
        dt = datetime.datetime.combine(date, datetime.time(0,0))
        return dt + datetime.timedelta(seconds=self.start)

    def getEndDate(self, date):
        dt = datetime.datetime.combine(date, datetime.time(0,0))
        return dt + datetime.timedelta(seconds=self.end)



class ScheduleDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;
                create table assistance.schedules (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    sdate date default now(),
                    sstart bigint,
                    send bigint,
                    weekday integer,
                    daily boolean default false,
                    created timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        s = Schedule()
        s.userId = r['user_id']
        s.start = r['sstart']
        s.end = r['send']
        s.date = r['sdate']
        s.weekday = r['weekday']
        s.daily = r['daily']
        return s

    @staticmethod
    def findByUserId(con, ids, startDate, endDate):
        assert isinstance(ids, list)
        cur = con.cursor()
        try:
            #cur.execute('select * from assistance.schedules where user_id in %s and sdate >= %s and sdate <= %s order by user_id, sdate, weekday', (tuple(ids), startDate, endDate))
            cur.execute('select * from assistance.schedules where user_id in %s order by user_id, sdate, weekday', (tuple(ids),))
            return [ ScheduleDAO._fromResult(r) for r in cur ]

        finally:
            cur.close()

    @staticmethod
    def findByUserIdInDate(con, id, date):
        cur = con.cursor()
        try:
            cur.execute('select * from assistance.schedules where user_id = %s and ((sdate <= %s and weekday = %s and daily = false) or (extract(dow from sdate) = weekday and daily = true)) order by sdate desc limit 1', (id, date, date.weekday()))
            if cur.rowcount <= 0:
                return None

            return ScheduleDAO._fromResult(cur.fetchone())

        finally:
            cur.close()
