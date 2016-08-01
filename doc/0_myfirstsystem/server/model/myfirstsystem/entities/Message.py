# -*- coding: utf-8 -*-
import uuid
from model.serializer.utils import JSONSerializable


class MessageDAO():

    @classmethod
    def _fromResult(cls, r):
        instance = Message()
        instance.id = r['id']
        instance.data = r['data']
   
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
                    INSERT INTO message (id, data)
                    VALUES (%(id)s, %(data)s;
                """, data)

            else:
                data = instance.__dict__
                cur.execute("""
                  UPDATE message
                  SET
                      data = %(data)s,
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
                SELECT * FROM message
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
                FROM message
            """)
            ids = [r['id'] for r in cur]
            return ids
        finally:
            cur.close()



class Message(JSONSerializable):

    dao = MessageDAO

    def __init__(self):
        self.id = None
        self.data = None
       

    def persist(self, con):
        return self.dao.persist(con, self)


    @classmethod
    def findById(cls, con, ids):
        return cls.dao.findById(con, ids)

    @classmethod
    def findAll(cls, con):
        return cls.dao.findAll(con)


