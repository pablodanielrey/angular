import dateutil, dateutil.tz, dateutil.parser, datetime
from dateutil.tz import tzlocal
import pytz

class Utils:

    @classmethod
    def _localizeLocal(cls, naive):
        if naive is None:
            return None
        tz = dateutil.tz.tzlocal()
        local = naive.replace(tzinfo=tz)
        return local

    @classmethod
    def _isNaive(cls, date):
        if date is None:
            return False
        return not ((date.tzinfo != None) and (date.tzinfo.utcoffset(date) != None))

    """ transforma un datetime naive a uno aware con la zona pasada """
    @classmethod
    def localize(cls, timezone, naive):
        tz = pytz.timezone(timezone)
        local = tz.localize(naive)
        return local

    """ retorna el datetime transformado a utc """
    @classmethod
    def awareToUtc(cls, date):
        return date.astimezone(pytz.utc)