# -*- coding: utf-8 -*-
import model.utils.DateTimeEncoder

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


class FDegree(Filter):

    def __init__(self):
        self.degree = 'Lic. En Economía'

    def _filter(self, inscriptions):
        return [ i for i in inscriptions if i.degree == self.degree ]

    def _toJson(self):
        return = self.degree

class FInscriptionDate(Filter):

    def __init__(self, date = None):
        if date is None:
            import datetime
            self.ffrom = datetime.datetime.now()
            self.to = datetime.datetime.now()
        else:
            self.date = date

    def _filter(self, inscriptions):
        return [ i for i in inscriptions if i.created.date().year == self.date.date().year ]

    def _fromJson(self, st):
        import json
        s = json.loads(st)
        self.ffrom = dateutils.parser(s['from'])

    def _toJson(self):
        import json
        return json.dumps(self, cls=DateTimeEncoder)



if __name__ == '__main__':

    import datetime
    fs = [ FInscriptionDate(), FDegree(), FInscriptionDate(datetime.datetime.now() - datetime.timedelta(hours = -1 * 24 * 365)) ]

    import jsonpickle
    import sys

    print(jsonpickle.encode(fs))
    sys.exit(1)

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
