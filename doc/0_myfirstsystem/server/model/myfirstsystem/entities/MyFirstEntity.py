# -*- coding: utf-8 -*-
import uuid
from model.serializer.utils import JSONSerializable


class MyFirstEntityDAO():

    @classmethod
    def _fromResult(cls, r):
        instance = Entity()
        instance.id = r['id']
        instance.field = r['field']
   
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
                    INSERT INTO myFirstTable (id, field)
                    VALUES (%(id)s, %(field)s;
                """, data)

            else:
                data = instance.__dict__
                cur.execute("""
                  UPDATE myFirstTable
                  SET
                      field = %(field)s,
                  WHERE id = %(id)s;
                """, data)

            return instance.id

        finally:
            cur.close()

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids, list)
        assert len(ids) > 0

        cur = con.cursor()
        try:
            cur.execute("""
                SELECT * FROM myFirstTable
                WHERE id in %s;
            """, (tuple(ids),))
            return [ cls._fromResult(r) for r in cur ]
        finally:
            cur.close()

  
    
            
    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT id
                FROM myFirstTable
            """)
            ids = [r['id'] for r in cur]
            return ids
        finally:
            cur.close()



class MyFirstEntity(JSONSerializable):

    dao = MyFirstEntityDAO

    def __init__(self):
        self.id = None
        self.field = None
       

    def persist(self, con):
        return self.dao.persist(con, self)


    @classmethod
    def findById(cls, con, ids):
        return cls.dao.findById(con, ids)

    @classmethod
    def findAll(cls, con):
        return cls.dao.findAll(con)


