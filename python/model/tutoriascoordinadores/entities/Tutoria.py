# -*- coding: utf-8 -*-
from model import Ids
from model.entity import Entity

class Tutoria(Entity):

    def __init__(self):
        self.id = None
        self.tutorId = None
        self.date = None
