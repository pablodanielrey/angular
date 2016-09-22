# -*- coding: utf-8 -*-
from model.serializer import JSONSerializable

class AbstractOffice(JSONSerializable):

    def __init__(self):
        self.name = ''

class Office(AbstractOffice):

    def __init__(self):
        super().__init__()
        self.parent = None

class Area(AbstractOffice):

    def __init__(self):
        super().__init__()
        self.parent()

class Dependency(AbstractOffice):

    def __init__(self):
        super().__init__()

class Funcion(JSONSerializable):

    def __init__(self):
        self.office = None
        self.position = 'Cumple función'
        self.user = None
