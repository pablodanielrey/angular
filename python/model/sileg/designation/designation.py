# -*- coding: utf-8 -*-
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
                    user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                    place_id VARCHAR NOT NULL REFERENCES sileg.place (id),
                    position_id VARCHAR NOT NULL REFERENCES sileg.position (id),
                    dstart DATE,
                    dend DATE
              );
              """
            cur.execute(sql)
        finally:
            cur.close()
          
          
    @classmethod
    def _fromResult(cls, r):
        c = Designation()
        c.id = r['id']
        c.userId = r['user_id']
        c.start = r['start']
        c.end = r['end']
        
        
        
    @classmethod
    def persist(cls, con, designation):
        assert designation is not None

        cur = con.cursor()
        try:
            if ((not hasattr(designation, 'id')) or (designation.id is None)):
                designation.id = str(uuid.uuid4())

            if len(designation.findById(con, [designation.id])) <=  0:

                r = designation.__dict__
                cur.execute("""
                    INSERT INTO sileg.designation (id, user_id, dstart, dend, created) 
                    VALUES (%(id)s, %(userId)s, %(start)s, %(end)s, %(created)s)
                """, r)
                            
            else:
                r = designation.__dict__
                cur.execute("""
                  UPDATE sileg.designation
                  SET user_id = %(userId)s, 
                  dstart = %(start)s, 
                  dend = %(end)s, 
                  WHERE id = %(id)s
                """, r)         
                              
            return designation.id

        finally:
            cur.close()
            

class Designation(JSONSerializable):

    def __init__(self, userId=None, start=None, end=None):
        self.id = None
        self.userId = userId
        self.start = start
        self.end = end
        self.created = datetime.datetime.now(tzlocal())
