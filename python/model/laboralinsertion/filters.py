# -*- coding: utf-8 -*-

import re

class Filter:

    fr = re.compile("^{'filter':'(?P<type>.*)', 'data':(?P<data>.*)}$")

    @staticmethod
    def _groupFilters(filters=[]):
        ''' agrupa los filtros por tipo (el nombre de la clase) '''
        groups = {}
        for f in filters:
            if f.__class__.__name__ not in groups:
                groups[f.__class__.__name__] = []
            groups[f.__class__.__name__].append(f)
        return groups

    @staticmethod
    def apply(ls, filters=[]):
        ''' aplica los filtros indicados a una lista de inscripciones '''
        groups = Filter._groupFilters(filters)
        result = None
        for k in groups.keys():
            s = set()
            for f in groups[k]:
                lss = f.filter(ls)
                s = s.union(lss)

            if result is None:
                result = s
            else:
                result = result.intersection(s)

        return result


    def filter(self, list):
        return self._filter(list)

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

    def _filter(self, inscriptions):
        return [ i for i in inscriptions if i.degree == self.degree ]


class FInscriptionDate(Filter):

    def __init__(self, date = None):
        if date is None:
            import datetime
            self.date = datetime.datetime.now()
        else:
            self.date = date

    def _toJson(self):
        return "'{}'".format(self.date.isoformat())

    @classmethod
    def _fromJson(cls, data):
        import dateutil.parser
        f = FInscriptionDate()
        date = data[1:][:-1]
        f.date = dateutil.parser.parse(date)
        return f

    def _filter(self, inscriptions):
        return [ i for i in inscriptions if i.created.date().year == self.date.date().year ]


if __name__ == '__main__':

    import datetime
    fs = [ FInscriptionDate(), FDegree(), FInscriptionDate(datetime.datetime.now() - datetime.timedelta(hours = -1 * 24 * 365)) ]

    from inscription import Inscription
    ins = Inscription()
    ins.degree = 'Lic. En Economía'
    ins.created = datetime.datetime.now()
    inss = []
    inss.append(ins)

    ins = Inscription()
    ins.degree = 'Lic. En Economía'
    ins.created = datetime.datetime.now() - datetime.timedelta(hours = -2 * 24 * 365)
    inss.append(ins)

    ins = Inscription()
    ins.degree = 'Lic. En Economí2a'
    ins.created = datetime.datetime.now()
    inss.append(ins)

    ins = Inscription()
    ins.degree = 'Lic. En Economía2'
    ins.created = datetime.datetime.now() - datetime.timedelta(hours = -2 * 24 * 365)
    inss.append(ins)

    ins = Inscription()
    ins.degree = 'Lic. En Economía'
    ins.created = datetime.datetime.now() - datetime.timedelta(hours = -1 * 24 * 365)
    inss.append(ins)

    fi = Filter.apply(inss, fs)
    for i in fi:
        print(i.__dict__)
