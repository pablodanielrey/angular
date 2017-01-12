# -*- coding: utf-8 -*-
from model.entity import Entity


class Company(Entity):
    ''' datos de una empresa de insercion laboral '''
    def __init__(self):
        self.name = ''
        self.detail = ''
        self.cuit = ''
        self.teacher = ''
        self.manager = ''
        self.address = ''
        self.id = ''
        self.contacts = []
        self.beginCM = None
        self.endCM = None
