# -*- coding: utf-8 -*-

import datetime, pytz

class Date:

    def isAware(self, date):
        if isinstance(date, datetime.date):
            return True
        return (date.tzinfo != None) and (date.tzinfo.utcoffset(date) != None)

    def isNaive(self, date):
        return not isAware(self, date)

    """ transforma un datetime naive a uno aware con la zona pasada """
    def localize(self, timezone, naive):
        tz = pytz.timezone(timezone)
        local = tz.localize(naive)
        return local

    """ retorna el datetime transformado a utc """
    def awareToUtc(self, date):
        return date.astimezone(pytz.utc)


    def utcNow(self):
        return datetime.datetime.now(datetime.timezone.utc)
