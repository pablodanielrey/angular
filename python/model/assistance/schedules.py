
import datetime
from model.serializer import JSONSerializable
from model.users.users import UserDAO
from model.assistance.assistanceDao import AssistanceDAO
from model.assistance.utils import Utils
from operator import attrgetter
import uuid

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
        self.special = False
        self.id = None
        self.isNull = False

    def isValid(self, date):
        if self.special:
            return date == self.date
        return (self.date <= date) and (self.weekday == date.weekday())

    def getStartDate(self, date):
        dt = datetime.datetime.combine(date, datetime.time(0,0))
        return Utils._localizeLocal(dt + datetime.timedelta(seconds=self.start))

    def getEndDate(self, date):
        dt = datetime.datetime.combine(date, datetime.time(0,0))
        return Utils._localizeLocal(dt + datetime.timedelta(seconds=self.end))

    def getScheduleSeconds(self):
        if self.end is None or self.start is None:
            return 0
        return self.end - self.start

    def persist(self, con):
        return ScheduleDAO.persist(con, self)

    def delete(self, con):
        return ScheduleDAO.delete(con, [self.id])

    @classmethod
    def findByUserId(cls, con, ids, startDate, endDate):
        return ScheduleDAO.findByUserId(con, ids, startDate, endDate)

    @classmethod
    def findByUserIdInDate(cls, con, userId, date):
        schedules = cls.findByUserId(con, [userId], date, date)
        schSorted = sorted([ sc for sc in schedules if sc.isValid(date)], key=attrgetter('date'), reverse=True)
        return [sc for sc in schSorted if sc.date == schSorted[0].date and sc.getScheduleSeconds() >= 0]

    @classmethod
    def findByUserIdInWeek(cls, con, userId, date, actualWeek = True):
        firstDate = date - datetime.timedelta(days=date.weekday()) if actualWeek else date
        result = {}
        for day in range(7):
            actual = firstDate + datetime.timedelta(days=day)
            result[actual] = cls.findByUserIdInDate(con, userId, actual)
        return result


class ScheduleDAO(AssistanceDAO):
    dependencies = [ UserDAO ]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;
                create table IF NOT EXISTS assistance.schedules (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    sdate date default now(),
                    sstart bigint,
                    send bigint,
                    weekday integer,
                    daily boolean default false,
                    special boolean default false,
                    is_null boolean default false,
                    created timestamptz default now()
                );

                CREATE TABLE IF NOT EXISTS assistance.schedules_history (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    sdate date default now(),
                    schedule_ids varchar[] not null,
                    created timestamptz default now()
                );
            """)

        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        s = Schedule()
        s.id = r['id']
        s.userId = r['user_id']
        s.start = r['sstart']
        s.end = r['send']
        s.date = r['sdate']
        s.weekday = r['weekday']
        s.daily = r['daily']
        s.special = r['special']
        s.isNull = r['is_null']
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

    @staticmethod
    def findUsersWithSchedule(con):
        """ lo creo para hacer unas pruebas pero puede servir para despues. es codig BETAAA """
        cur = con.cursor()
        try:
            cur.execute('select distinct user_id from assistance.schedules')
            return [ c[0] for c in cur ]

        finally:
            cur.close()

    @classmethod
    def persist(cls, con, sch):
        assert sch is not None

        cur = con.cursor()
        try:
            sch.id = str(uuid.uuid4())
            r = sch.__dict__
            cur.execute('insert into assistance.schedules (id, user_id, sdate, sstart, send, weekday, daily, special, is_null) '
                        'values ( %(id)s, %(userId)s, %(date)s, %(start)s, %(end)s, %(weekday)s, %(daily)s, %(special)s, %(isNull)s)', r)
            return sch.id
        finally:
            cur.close()


    @classmethod
    def delete(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('delete from assistance.schedules where id in %s', (tuple(ids),))
            return ids

        finally:
            cur.close()


class ScheduleHistoryDAO(AssistanceDAO):
    dependencies = [ UserDAO ]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;

                CREATE TABLE IF NOT EXISTS assistance.schedules_history (
                    id varchar primary key,
                    user_id varchar not null references profile.users (id),
                    sdate date default now(),
                    schedule_ids varchar[] not null,
                    description varchar,
                    created timestamptz default now()
                );
            """)

        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        s = ScheduleHistory()
        s.id = r['id']
        s.userId = r['user_id']
        s.date = r['sdate']
        s.schedules = r['schedule_ids']
        s.created = r['created']
        s.description = r['description']
        return s

    @classmethod
    def persist(cls, con, s):
        cur = con.cursor()
        try:
            s.id = str(uuid.uuid4())
            param = s.__dict__
            cur.execute('insert into assistance.schedules_history (id, user_id, sdate, schedule_ids) '
                        'values ( %(id)s, %(userId)s, %(date)s, %(schedules)s)', param)
            return s.id
        finally:
            cur.close()

    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            cur.execute('select id from assistance.schedules_history')
            return [c['id'] for c in cur]

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids=[]):
        assert isinstance(ids, list)
        if len(ids) <= 0:
            return []

        cur = con.cursor()
        try:
            cur.execute('select * from assistance.schedules_history where id in %s', (tuple(ids),))
            return [cls._fromResult(c) for c in cur]

        finally:
            cur.close()


    @classmethod
    def delete(cls, con, ids):
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('delete from assistance.schedules_history where id in %s', (tuple(ids),))
            return ids

        finally:
            cur.close()

class ScheduleHistory(JSONSerializable):

    dao = ScheduleHistoryDAO

    def __init__(self):
        self.id = None
        self.userId = None
        self.date = None
        self.schedules = []
        self.created = None
        self.description = ''

    def persist(self, con):
        return self.dao.persist(con, self)

    def delete(self, con):
        return self.dao.delete(con, [self.id])

    @classmethod
    def findAll(cls, con):
        return cls.dao.findAll(con)

    @classmethod
    def findById(cls, con, ids):
        return cls.dao.findById(con, ids)
