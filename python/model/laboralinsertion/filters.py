# -*- coding: utf-8 -*-
import re
import logging
import json
import sys

from model.utils import DateTimeEncoder

class Filter:

    ls = re.compile("{(.*?)}")
    #frt = re.compile("^{['|\"]filter['|\"]:['|\"](?P<type>.*)['|\"], ['|\"]data['|\"]:(?P<data>.*)}$")
    frt = re.compile(".*['|\"]\s*filter\s*['|\"]\s*:\s*['|\"]\s*(?P<type>.*?)['|\"].*")
    frd = re.compile(".*['|\"]\s*data\s*['|\"]\s*:\s*(?P<data>{.*?}).*")

    @staticmethod
    def toJsonList(ls):
        return '[' + ','.join([ s.toJson() for s in ls ]) + ']'

    @classmethod
    def _fromJsonList(cls, l):
        ls = []
        for i in l:
            logging.debug(str(i))
            i = str(i).replace("'", "\"")
            o = cls.fromJson(i)
            if o is not None:
                logging.debug('deseializado')
                ls.append(o)
        return ls

    @classmethod
    def fromJsonList(cls, s):
        logging.debug('fromJsonList {}'.format(s))
        import json
        sls = json.loads(s)
        logging.debug(sls)
        return cls._fromJsonList(sls)

    @classmethod
    def fromJson(cls, s):

        logging.debug('deserializando')
        logging.debug(s)

        m = cls.frt.match(s)
        if not m:
            return None

        m2 = cls.frd.match(s)
        if not m2:
            return None

        t = m.group('type')
        d = m2.group('data')

        ''' deserializa el objeto desde json '''
        for sub in cls.__subclasses__():
            logging.debug('chequeando {} == {}'.format(t, sub.__name__))
            if t == sub.__name__:
                o = sub._fromJson(d)
                if o is not None:
                    return o
        return None

    @classmethod
    def _fromJson(cls, s):
        d = cls()
        d.__dict__ = json.loads(s)
        return d

    def toJson(self):
        return "{{\"filter\":\"{}\", \"data\":{}}}".format(self.__class__.__name__, self._toJson())

    def _toJson(self):
        import json
        return json.dumps(self.__dict__)

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
    def apply(con, ls, filters=[]):
        ''' aplica los filtros indicados a una lista de inscripciones '''
        groups = Filter._groupFilters(filters)
        result = None
        for k in groups.keys():
            s = set()
            for f in groups[k]:
                lss = f.filter(con, ls)
                s = s.union(lss)

            if result is None:
                result = s
            else:
                result = result.intersection(s)

        return result

    def filter(self, con, ls):
        return self._filter(con, ls)


class FInscriptionDate(Filter):

    def __init__(self):
        self.ffrom = None
        self.to = None

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if i.created >= self.ffrom and i.created <= self.to ]

    def _toJson(self):
        import json
        return json.dumps(self.__dict__, cls=DateTimeEncoder)

    @classmethod
    def _fromJson(cls, data):
        import json
        #import dateutil.parser
        f = FInscriptionDate()
        logging.debug(data)
        f.__dict__ = json.loads(data)
        #d.ffrom = dateutil.parser.parse(d.ffrom)
        #d.to = dateutil.parser.parse(d.to)
        return d


class FDegree(Filter):

    def __init__(self):
        self.degree = 'Lic. En Economía'

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if i.degree == self.degree ]

    @classmethod
    def _fromJson(cls, s):
        d = FDegree()
        d.__dict__ = json.loads(s)
        return d


class FOffer(Filter):

    def __init__(self):
        self.offer = ''

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if i.workType == self.offer ]


class FWorkExperience:

    def __init__(self):
        self.workExperience = True

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if i.workExperience == self.workExperience ]


class FGenre(Filter):

    def __init__(self):
        self.genre = 'Masculino'

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if i.getUser(con).genre == self.genre ]


class FAge(Filter):

    def __init__(self):
        self.age = 0

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if FAge._age(i.getUser(con).birthdate) == self.age ]

    @staticmethod
    def _age(birthdate):
        import datetime
        return (datetime.datetime.now() - birthdate).year


class FPriority:

    def __init__(self):
        self.ffrom = 0
        self.to = 0


class Filters:

    @staticmethod
    def getFilters():
        fs = [ FInscriptionDate(), FDegree() ]
        return jsonpickle.encode(fs)
