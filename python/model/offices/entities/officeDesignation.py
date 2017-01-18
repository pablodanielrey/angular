# -*- coding: utf-8 -*-
from model import Ids
from model.designation.entities.designation import Designation

class OfficeDesignation(Designation):

    def __init__(self):
        super().__init__();
        self.positionId = "1"
