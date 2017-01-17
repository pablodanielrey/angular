# -*- coding: utf-8 -*-
from model import Ids
from model.designation.entities.place import Place

class TeachingPlace(Place):

    def __init__(self):
        super().__init__();
        self.telephone = None
        self.email = None
