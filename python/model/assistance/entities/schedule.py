# -*- coding: utf-8 -*-
from model import Ids
from model.entity import Entity

class Schedule(Entity):

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


    @classmethod
    def deleteByIds(cls, ctx, ids):
      return ctx.dao(self).deleteByIds(ctx, ids)

    @classmethod
    def findByUserIdsInDates(cls, ctx, userIds, startDate, endDate):
        """
        buscar por userIds en cierto rango de fechas
        parameters:
          ids Identificadores de usuario
          startDate fecha de inicio
          endDate fecha de fin
        """
        return Ids(ctx.dao(self).findByUserIdsInDates(con, userIds, startDate, endDate))

    @classmethod
    def findByUserIdInDate(cls, ctx, userId, date):
        """
        buscar por usuario en una determinada fecha
        parameters:
          ids Identificadores de usuario
          startDate fecha de inicio
          endDate fecha de fin
        """
        schedulesIds = cls.findByUserIdsInDates(ctx, [userId], date, date).fetch(ctx)
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
