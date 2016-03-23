# -*- coding: utf-8 -*-
import re
import logging
import json
import sys

from model.laboralinsertion.languages import LanguageDAO

class Filter:

    @classmethod
    def fromMapList(cls, ls):
        result = []
        for f in ls:
            for sub in cls.__subclasses__():
                if f['filter'] == sub.__name__:
                    o = sub._fromMap(f['data'])
                    if o is not None:
                        result.append(o)
        return result

    @classmethod
    def _fromMap(cls, m):
        try:
            c = cls()
            c.__dict__ = m
            return c
        except Exception as e:
            logging.exception(e)
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


class FDegree(Filter):

    def __init__(self):
        self.degree = 'Lic. En Economía'

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if i.degree == self.degree ]


class FOffer(Filter):

    def __init__(self):
        self.offer = ''

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if i.workType == self.offer ]


class FWorkExperience(Filter):

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
        self.beginAge = 0
        self.endAge = 0

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if FAge._age(i.getUser(con).birthdate) >= self.beginAge and FAge._age(i.getUser(con).birthdate) <= self.endAge ]

    @staticmethod
    def _age(birthdate):
        import datetime
        if (birthdate is None):
            return 0
        return (datetime.date.today() - birthdate).days / 365


class FResidence(Filter):

    def __init__(self):
        self.city = 'La Plata'

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if i.getUser(con).residence_city == self.city ]


class FCity(Filter):

    def __init__(self):
        self.city = 'La Plata'

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if i.getUser(con).city == self.city ]

class FTravel(Filter):

    def __init__(self):
        self.travel = True

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if i.travel == self.travel ]

class FLanguage(Filter):

    def __init__(self):
        self.language = "Inglés"
        self.level = None

    def _filter(self, con, inscriptions):
        return [ i for i in inscriptions if FLanguage._includeLanguages(con, self.language, self.level, i.getLanguages(con)) ]

    @staticmethod
    def _includeLanguages(con, language, level, languages):
        for lid in languages:
            l = LanguageDAO.findById(con, lid)
            if l.name == language and (level == None or l.level == level):
                return True
        return False

class FPriority:

    def __init__(self):
        self.ffrom = 0
        self.to = 0
