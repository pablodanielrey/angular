
import logging
from model.sileg.place.place import Place

class SilegModel:

    @staticmethod
    def getPlaceById(con, ids):
        return Place.findById(con, ids)
      

   
