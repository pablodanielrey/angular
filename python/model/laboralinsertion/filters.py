# -*- coding: utf-8 -*-

import re

class Filter:

    fr = re.compile("^{'filter':'(?P<type>.*)', 'data':(?P<data>.*)}$")

    def toJson(self):
        return "{{'filter':'{}', 'data':{}}}".format(self.__class__.__name__, self._toJson())

    @classmethod
    def fromJson(cls, s):
        m = cls.fr.match(s)
        if not m:
            return None

        t = m.group('type')
        d = m.group('data')

        ''' deserializa el objeto desde json '''
        for sub in cls.__subclasses__():
            o = sub._fromJson(t,d)
            if o is not None:
                return o
        return None


class FInscriptionDate(Filter):

    def __init__(self):
        import datetime
        self.date = datetime.datetime.now()

    def _toJson(self):
        return "'{}'".format(self.date.isoformat())

    @classmethod
    def _fromJson(cls, t, data):
        if cls.__name__ != t:
            return None

        import dateutil.parser
        f = FInscriptionDate()
        date = data[1:][:-1]
        f.date = dateutil.parser.parse(date)
        return f



if __name__ == '__main__':
    f = FInscriptionDate()
    import datetime
    f.date = datetime.datetime.now()
    s = f.toJson()
    print(s)
    ft = Filter.fromJson(s)
    print(ft.__class__.__name__)
    print(ft.toJson())
