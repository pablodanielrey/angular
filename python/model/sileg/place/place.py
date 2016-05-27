# -*- coding: utf-8 -*-
from model.sileg.silegdao import SilegDAO
from model.serializer.utils import JSONSerializable

class PlaceDAO(SilegDAO):

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS sileg;

              CREATE TABLE IF NOT EXISTS sileg.place (
                    id VARCHAR PRIMARY KEY,
                    description VARCHAR NOT NULL
              );
              """
            cur.execute(sql)
        finally:
            cur.close()
            
   


class Place(JSONSerializable):

    dao = PlaceDAO
    
    def __init__(self):
        self.id = None
        self.description = None

    
    @classmethod
    def persist(self, con):
        return dao.persist(con, self)
        
        
    @classmethod
    def findAll(cls, con):
        return dao.findAll(con)


    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids,list)
        ret = [ dao.findById(con, id) for id in ids ]
        return ret
   
