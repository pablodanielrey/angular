# -*- coding: utf-8 -*-
from model.entity import Entity

class Place(Entity):

    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.parent = None
        self.public = None
        self.removed = None
