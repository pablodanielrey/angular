# -*- coding: utf-8 -*-
import uuid
from model.sileg.silegdao import SilegDAO
from model.serializer.utils import JSONSerializable
from model.users.users import UserDAO
from model.sileg.position.position import PositionDAO
from model.sileg.place.place import PlaceDAO


class DesignationDAO(SilegDAO):

    dependencies = [PlaceDAO, PositionDAO, UserDAO]
    
    
    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS sileg;

              CREATE TABLE IF NOT EXISTS sileg.designation (
                    id VARCHAR PRIMARY KEY,
                    dstart DATE,
                    dend DATE,
                    dout DATE,
                    user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                    place_id VARCHAR NOT NULL REFERENCES sileg.place (id),
                    position_id VARCHAR NOT NULL REFERENCES sileg.position (id)
                    
              );
              """
            cur.execute(sql)
        finally:
            cur.close()
          
          
    @classmethod
    def _fromResult(cls, r):
        instance = Designation()
        instance.id = r['id']
        instance.start = r['dstart']
        instance.end = r['dend']
        instance.out = r['dout']
        instance.userId = r['user_id']
        instance.placeId = r["place_id"]
        instance.positionId = r["position_id"]
        
        
        
    @classmethod
    def persist(cls, con, instance):        
        assert instance is not None
        
        cur = con.cursor()
        try:
            if ((not hasattr(instance, 'id')) or (instance.id is None)):
                instance.id = str(uuid.uuid4())
            
            
            if len(instance.findById(con, [instance.id])) <=  0:
                data = instance.__dict__
                cur.execute("""
                    INSERT INTO sileg.designation (id, dstart, dend, dout, user_id, position_id, place_id) 
                    VALUES (%(id)s, %(start)s, %(end)s, %(out)s, %(userId)s, %(positionId)s, %(placeId)s)
                """, data)
                
            else:
                data = instance.__dict__
                cur.execute("""
                  UPDATE sileg.designation
                  SET 
                      dstart = %(start)s, 
                      dend = %(end)s, 
                      dout = %(out)s, 
                      user_id = %(userId)s, 
                      position_id = %(positionId)s, 
                      place_id = %(placeId)s
                  WHERE id = %(id)s
                """, data) 
                
            return instance.id

        finally:
            cur.close()
        
    @classmethod
    def findById(cls, con, ids):           
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute("""
                SELECT * FROM sileg.designation 
                WHERE id in %s
            """, (tuple(ids),))
            return [ cls._fromResult(con, r) for r in cur ]
        finally:
            cur.close()
  
      
            

class Designation(JSONSerializable):

    dao = DesignationDAO

    def __init__(self):
        self.id = None
        self.start = None
        self.end = None
        self.out = None        
        self.userId = None
        self.placeId = None
        self.positionId = None


    def persist(self, con):
        return self.dao.persist(con, self)


    @classmethod
    def findById(cls, con, ids):
        return cls.dao.findById(con, ids)
        
 
