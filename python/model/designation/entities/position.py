# -*- coding: utf-8 -*-
from model.entity import Entity

class Position(Entity):

    SUPPORT = 0
    NONTEACHING = 1
    TEACHING = 2

    def __init__(self):
        self.id = '1'
        self.position = 'Cumple función'
        self.type = self.SUPPORT
