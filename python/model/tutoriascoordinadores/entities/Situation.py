# -*- coding: utf-8 -*-
from model import Ids
from model.entity import Entity

class Situation(Entity):

    def __init__(self):
        self.id = None
        self.situation = None
        self.tutoringId = None
        self.userId = None
