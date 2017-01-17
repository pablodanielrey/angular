# -*- coding: utf-8 -*-
from model import Ids
from model.designation.entities.position import Position

class TeachingPosition(Position):

    def __init__(self):
        super().__init__();
        self.detail = None
        self.type = 2
