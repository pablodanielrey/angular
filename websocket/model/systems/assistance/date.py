# -*- coding: utf-8 -*-

import datetime, pytz
import dateutil, dateutil.tz
import logging

class Date:

    def isAware(self, date):
        return (date.tzinfo != None) and (date.tzinfo.utcoffset(date) != None)

    def isNaive(self, date):
        return not self.isAware(date)

    """ transforma un datetime naive a uno aware con la zona pasada """
    def localize(self, timezone, naive):
        tz = pytz.timezone(timezone)
        local = tz.localize(naive)
        return local

    def localizeLocal(self,naive):
        tz = dateutil.tz.tzlocal()
        local = tz.localize(naive)
        return local

    """ retorna el datetime transformado a utc """
    def awareToUtc(self, date):
        return date.astimezone(pytz.utc)


    def utcNow(self):
        return datetime.datetime.now(pytz.utc)


    def isUTC(self,date):
        logging.debug(date.tzinfo)
        return date.tzinfo != None and date.tzinfo.utcoffset(date) == datetime.timedelta(0)
