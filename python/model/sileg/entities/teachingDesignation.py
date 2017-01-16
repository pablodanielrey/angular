# -*- coding: utf-8 -*-
from model import Ids
from model.designation.entities.designation import Designation

class TeachingDesignation(Designation):

    def __init__(self):
        super.__init__();
        self.out = None
        self.resolution = None
        self.record = None
