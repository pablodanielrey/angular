# -*- coding: utf-8 -*-
import uuid
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
                    description VARCHAR NOT NULL,
                    dependence VARCHAR REFERENCES sileg.place (id), 
                    type VARCHAR
              );
              """
            cur.execute(sql)
        finally:
            cur.close()
            
            
    @classmethod
    def _fromResult(cls, r):
        instance = Place()
        instance.id = r['id']
        instance.description = r['description']
        instance.dependence = r['dependence']
        instance.type = r['type']
        return instance
        
        
    @classmethod
    def persist(cls, con, place):        
        assert place is not None
        
        cur = con.cursor()
        try:
            if ((not hasattr(place, 'id')) or (place.id is None)):
                place.id = str(uuid.uuid4())
            
            
            if len(place.findById(con, [place.id])) <=  0:
                data = place.__dict__
                cur.execute("""
                    INSERT INTO sileg.place (id, description, dependence, type)
                    VALUES (%(id)s, %(description)s, %(dependence)s, %(type)s)
                """, data)
                
            else:
                data = place.__dict__
                cur.execute("""
                    UPDATE sileg.place
                    SET description = %(description)s, 
                        dependence = %(dependence)s, 
                        type = %(type)s
                    WHERE id = %(id)s;
                """, data)
                
            return place.id

        finally:
            cur.close()


    @classmethod
    def findById(cls, con, ids):           
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute("""
                SELECT * FROM sileg.place 
                WHERE id in %s
            """, (tuple(ids),))
            return [ cls._fromResult(r) for r in cur ]
        finally:
            cur.close()
   
    @classmethod
    def findByUnique(cls, con, description, dependence, type):
        cur = con.cursor()
        
        sql = "SELECT id FROM sileg.place WHERE description = '" + description + "' "
        
        dependence = "AND dependence IS NULL " if dependence is None else "AND dependence = '" + dependence + "' "
        sql = sql + dependence
        
        type = "AND type IS NULL;" if type is None else "AND type = '" + type + "';"
        sql = sql + type
           
        try:
            cur.execute(sql)
            r = cur.fetchone()
            return None if r is None else r ["id"]
            
        finally:
            cur.close()
   
            

class Place(JSONSerializable):

    dao = PlaceDAO
    
    def __init__(self):
        self.id = None
        self.description = None
        self.dependence = None
        self.type = None


    def persist(self, con):
        return self.dao.persist(con, self)
        

    @classmethod
    def findAll(cls, con):
        return cls.dao.findAll(con)


    @classmethod
    def findById(cls, con, ids):
        return cls.dao.findById(con, ids)
        
    @classmethod 
    def findByUnique(cls, con, description, dependence = None, type = None):
        return cls.dao.findByUnique(con, description, dependence, type)
