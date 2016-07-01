# -*- coding: utf-8 -*-
import uuid
from model.sileg.silegdao import SilegDAO
from model.serializer.utils import JSONSerializable
from model.sileg.designation.designation import DesignationDAO


class LicenceDAO(SilegDAO):

    dependencies = [DesignationDAO]
    
    
    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS sileg;

              CREATE TABLE IF NOT EXISTS sileg.licence (
                    id VARCHAR PRIMARY KEY,
                    dstart DATE NOT NULL,
                    dend DATE,
                    dout DATE,
                    description VARCHAR NOT NULL,
                    salary BOOLEAN,
                    designation_id VARCHAR NOT NULL REFERENCES sileg.designation (id),
                    old_id INTEGER NOT NULL,
                    old_type VARCHAR NOT NULL,
                    replace_id VARCHAR REFERENCES sileg.licence (id),
                    UNIQUE(old_id, old_type)
              );
              """
            cur.execute(sql)
        finally:
            cur.close()
          
          
    @classmethod
    def _fromResult(cls, r):
        instance = Licence()
        instance.id = r['id']
        instance.start = r['dstart']
        instance.end = r['dend']
        instance.out = r["dout"]
        instance.description = r["description"]
        instance.salary = r["salary"]        
        instance.designationId = r['designation_id']
        instance.replaceId = r["replace_id"]
                
        instance.oldId = r["old_id"]
        instance.oldType = r["old_type"]

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
                    INSERT INTO sileg.licence (id, dstart, dend, dout, description, salary, designation_id, replace_id, old_id, old_type) 
                    VALUES (%(id)s, %(start)s, %(end)s, %(out)s, %(description)s, %(salary)s, %(designationId)s, %(replaceId)s, %(oldId)s, %(oldType)s);
                """, data)
                
            else:
                data = instance.__dict__
                cur.execute("""
                  UPDATE sileg.licence
                  SET 
                      dstart = %(start)s, 
                      dend = %(end)s, 
                      dout = %(out)s, 
                      description = %(description)s,
                      salary = %(salary)s,
                      designation_id = %(designationId)s,
                      replace_id = %(replaceId)s,
                      
                      old_id = %(oldId)s,
                      old_type = %(oldType)s
                  WHERE id = %(id)s;
                """, data) 
                
            return instance.id

        finally:
            cur.close()
        
    @classmethod
    def findById(cls, con, ids):           
        assert isinstance(ids, list)
        if len(ids) == 0:
            return []

        cur = con.cursor()
        try:
            cur.execute("""
                SELECT * FROM sileg.licence 
                WHERE id in %s;
            """, (tuple(ids),))
            return [ cls._fromResult(r) for r in cur ]
        finally:
            cur.close()
            
    @classmethod
    def findByDesignationId(cls, con, designationId):    

        cur = con.cursor()
        try:
            cur.execute("""
                SELECT id 
                FROM sileg.licence 
                WHERE designation_id = %s;
            """, (designationId,))
            return [r['id'] for r in cur]

        finally:
            cur.close()
  
  
    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT id 
                FROM sileg.licence;
            """)
            ids = [r['id'] for r in cur]
            return ids
        finally:
            cur.close()
            
    @classmethod
    def findAllActive(cls, con):
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT id 
                FROM sileg.licence
                WHERE dout IS NULL;
            """)
            ids = [r['id'] for r in cur]
            return ids
        finally:
            cur.close()
            
            
    @classmethod
    def findAllHistory(cls, con):
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT id 
                FROM sileg.licence
                WHERE dout IS NOT NULL;
            """)
            ids = [r['id'] for r in cur]
            return ids
        finally:
            cur.close()
                                  
              
    @classmethod
    def findByUnique(cls, con, oldId, oldType):
        cur = con.cursor()
           
        try:
            cur.execute("""
                SELECT id FROM sileg.licence 
                WHERE old_id = %s AND old_type = %s;
            """, (oldId, oldType))
            r = cur.fetchone()
            return None if r is None else r ["id"]
            
        finally:
            cur.close()
            
            
    @classmethod
    def numRowsByOldType(cls, con, oldType):
        cur = con.cursor()
    
        try:
            cur.execute("""
                SELECT count(*)
                FROM sileg.licence 
                WHERE old_type = %s
            """, (oldType,))
            r = cur.fetchone()
            return None if r is None else r ["count"]
            
        finally:
            cur.close()

class Licence(JSONSerializable):

    dao = LicenceDAO

    def __init__(self):
        self.id = None
        self.start = None
        self.end = None
        self.out = None
        self.description = None
        self.salary = None
        self.designationId = None
        self.replaceId = None
                
        self.oldId = None
        self.oldType = None


    def persist(self, con):
        return self.dao.persist(con, self)


    @classmethod
    def findById(cls, con, ids):
        return cls.dao.findById(con, ids)
        
    @classmethod
    def findAll(cls, con):
        return cls.dao.findAll(con)
        
    @classmethod
    def findAllActive(cls, con):
        return cls.dao.findAllActive(con)
        
    @classmethod
    def findAll(cls, con):
        return cls.dao.findAllHistory(con)                
        
    @classmethod
    def findByDesignationId(cls, con, designationId):
        return cls.dao.findByDesignationId(con, designationId)      
        
    @classmethod 
    def findByUnique(cls, con, oldId, oldType):
        return cls.dao.findByUnique(con, oldId, oldType)
  
    @classmethod 
    def numRowsByOldType(cls, con, oldType):
        return cls.dao.numRowsByOldType(con, oldType)
  
    
