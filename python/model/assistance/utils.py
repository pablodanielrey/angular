import dateutil, dateutil.tz, dateutil.parser, datetime
from dateutil.tz import tzlocal
class Utils:

    @classmethod
    def _localizeLocal(cls,naive):
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
