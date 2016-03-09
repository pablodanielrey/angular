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
            if sub.__name__ != t:
                continue

            o = sub._fromJson(d)
            if o is not None:
                return o
        return None


class FDegree(Filter):

    def __init__(self):
        self.degree = 'Lic. En Economía'

    def _toJson(self):
        return "'{}'".format(self.degree)

    @classmethod
    def _fromJson(cls, data):
        d = FDegree()
        d.degree = data[1:][:-1]
        return d


class FInscriptionDate(Filter):

    def __init__(self):
        import datetime
        self.date = datetime.datetime.now()

    def _toJson(self):
        return "'{}'".format(self.date.isoformat())

    @classmethod
    def _fromJson(cls, data):
        import dateutil.parser
        f = FInscriptionDate()
        date = data[1:][:-1]
        f.date = dateutil.parser.parse(date)
        return f


if __name__ == '__main__':

    fs = [ FInscriptionDate(), FDegree() ]
    for f in fs:
        s = f.toJson()
        print(s)
        ft = Filter.fromJson(s)
        print(ft.__class__.__name__)
        print(ft.toJson())
