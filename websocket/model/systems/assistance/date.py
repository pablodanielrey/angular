# -*- coding: utf-8 -*-

import datetime, pytz
import dateutil, dateutil.tz, dateutil.parser
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

    """ supnog que la fecha esta en la timezone local. """
    def localizeLocal(self,naive):
        tz = dateutil.tz.tzlocal()
        local = naive.replace(tzinfo=tz)
        return local

    """ retorna el datetime transformado a utc """
    def awareToUtc(self, date):
        return date.astimezone(pytz.utc)


    def now(self):
        date = datetime.datetime.now()
        return self.localizeLocal(date)

    def utcNow(self):
        return datetime.datetime.now(pytz.utc)


    def isUTC(self,date):
        logging.debug(date.tzinfo)
        return date.tzinfo != None and date.tzinfo.utcoffset(date) == datetime.timedelta(0)


    """
        parsea una fecha y hora y la retorna el la zona local del servidor.
        si viene sin timezone entonces supone que esta en la zona del server.
    """
    def parse(self,datestr):
        dt = dateutil.parser.parse(datestr)
        if self.isNaive(dt):
            dt = self.localizeLocal(dt)
        return dt
