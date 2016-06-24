# -*- coding: utf-8 -*-
from model.sileg.place.place import Place

class SilegModel:
    def getPlaceById(self, con, ids):
        return Place.findById(ids)

