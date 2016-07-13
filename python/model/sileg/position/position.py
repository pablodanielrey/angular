# -*- coding: utf-8 -*-
import uuid
from model.sileg.silegdao import SilegDAO
from model.serializer.utils import JSONSerializable

class PositionDAO(SilegDAO):
    
    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS sileg;

              CREATE TABLE IF NOT EXISTS sileg.position (
                    id VARCHAR PRIMARY KEY,
                    description VARCHAR NOT NULL,
                    detail VARCHAR
              );"""
            cur.execute(sql)
            
        finally:
            cur.close()
            
    @classmethod
    def _fromResult(cls, r):
        instance = Position()
        instance.id = r['id']
        instance.description = r['description']
        instance.detail = r['detail']
        return instance 
   
   
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
                    INSERT INTO sileg.position (id, description, detail)
                    VALUES (%(id)s, %(description)s, %(detail)s)
                """, data)
                
            else:
                data = instance.__dict__
                cur.execute("""
                    UPDATE sileg.position
                    SET description = %(description)s, 
                        detail = %(detail)s
                    WHERE id = %(id)s;
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
                SELECT * FROM sileg.position 
                WHERE id in %s
            """, (tuple(ids),))
            return [ cls._fromResult(r) for r in cur ]
        finally:
            cur.close()
   
    @classmethod
    def findByUnique(cls, con, description, detail):
        cur = con.cursor()
           
        try:
            cur.execute("""
                SELECT id FROM sileg.position 
                WHERE description = %s AND detail = %s
            """, (description,detail))
            r = cur.fetchone()
            return None if r is None else r ["id"]
            
        finally:
            cur.close()
            
            

    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
           
        try:
            cur.execute("""
                SELECT id 
                FROM sileg.position 
            """)
            return [r['id'] for r in cur]
            
        finally:
            cur.close()          
            
            
class Position(JSONSerializable):

    dao = PositionDAO
    
    def __init__(self):
        self.id = None
        self.description = None
        self.detail = None

    
    def persist(self, con):
        return self.dao.persist(con, self)
        
        
    @classmethod
    def findAll(cls, con):
        return cls.dao.findAll(con)


    @classmethod
    def findById(cls, con, ids):
        return cls.dao.findById(con, ids)

    @classmethod 
    def findByUnique(cls, con, description, detail):
        return cls.dao.findByUnique(con, description, detail)
        
        
    @classmethod 
    def findAll(cls, con):
        return cls.dao.findAll(con)
