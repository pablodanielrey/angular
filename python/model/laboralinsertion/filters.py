# -*- coding: utf-8 -*-
import jsonpickle
class Filter:

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


class FInscriptionDate(Filter):

    def __init__(self, date = None):
        if date is None:
            import datetime
            self.date = datetime.datetime.now()
        else:
            self.date = date

    def _filter(self, inscriptions):
        return [ i for i in inscriptions if i.created.date().year == self.date.date().year ]

class FWorkExperience(Filter):

    def __init__(self):
        self.workExperience = True


class FPriority(Filer):

    def __init__(self):
        self.ffrom = 0
        self.to = 0


class Filters:

    @staticmethod
    def getFilters():
        fs = [ FInscriptionDate(), FDegree() ]
        return jsonpickle.encode(fs)





if __name__ == '__main__':

    import datetime
    fs = [ FInscriptionDate(), FDegree(), FInscriptionDate(datetime.datetime.now() - datetime.timedelta(hours = -1 * 24 * 365)) ]

    import jsonpickle
    import sys

    print(jsonpickle.encode(fs))
    # sys.exit(1)

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
        json = jsonpickle.encode(i)
        print(json)
