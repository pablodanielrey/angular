# -*- coding: utf-8 -*-
import uuid
from model.sileg.silegdao import SilegDAO
from model.serializer.utils import JSONSerializable
from model.users.users import UserDAO
from model.sileg.position.position import PositionDAO
from model.sileg.place.place import PlaceDAO


class DesignationDAO(SilegDAO):

    dependencies = [PlaceDAO, PositionDAO, UserDAO]
    _TYPE = 'original'

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS sileg;

              CREATE TABLE IF NOT EXISTS sileg.designation (
                    id VARCHAR PRIMARY KEY,
                    dstart DATE NOT NULL,
                    dend DATE,
                    dout DATE,
                    description VARCHAR NOT NULL,
                    user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                    place_id VARCHAR NOT NULL REFERENCES sileg.place (id),
                    position_id VARCHAR NOT NULL REFERENCES sileg.position (id),
                    replace_id VARCHAR REFERENCES sileg.designation (id),
                    old_id INTEGER NOT NULL,
                    old_type VARCHAR NOT NULL,
                    UNIQUE(old_id, old_type)

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
        instance.out = r["dout"]
        instance.description = r["description"]
        instance.userId = r['user_id']
        instance.placeId = r["place_id"]
        instance.positionId = r["position_id"]
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
                    INSERT INTO sileg.designation (id, dstart, dend, dout, description, user_id, position_id, place_id, replace_id, old_id, old_type)
                    VALUES (%(id)s, %(start)s, %(end)s, %(out)s, %(description)s, %(userId)s, %(positionId)s, %(placeId)s, %(replaceId)s, %(oldId)s, %(oldType)s);
                """, data)

            else:
                data = instance.__dict__
                cur.execute("""
                  UPDATE sileg.designation
                  SET
                      dstart = %(start)s,
                      dend = %(end)s,
                      dout = %(out)s,
                      description = %(description)s,
                      user_id = %(userId)s,
                      position_id = %(positionId)s,
                      place_id = %(placeId)s,
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
        assert len(ids) > 0

        cur = con.cursor()
        try:
            cur.execute("""
                SELECT * FROM sileg.designation
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
                FROM sileg.designation
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
                FROM sileg.designation
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
                FROM sileg.designation
                WHERE dout IS NOT NULL;
            """)
            ids = [r['id'] for r in cur]
            return ids
        finally:
            cur.close()


    @classmethod
    def numRowsByOldType(cls, con, oldType):
        cur = con.cursor()

        try:
            cur.execute("""
                SELECT count(*)
                FROM sileg.designation
                WHERE old_type = %s
            """, (oldType,))
            r = cur.fetchone()
            return None if r is None else r ["count"]

        finally:
            cur.close()

    @classmethod
    def findByUnique(cls, con, oldId, oldType):
        cur = con.cursor()

        try:
            cur.execute("""
                SELECT id FROM sileg.designation
                WHERE old_id = %s AND old_type = %s;
            """, (oldId, oldType))
            r = cur.fetchone()
            return None if r is None else r ["id"]

        finally:
            cur.close()


class ProrogationDAO(DesignationDAO):

    _TYPE = 'prorroga'

    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT id
                FROM sileg.designation
                WHERE description == %s
            """, (cls._TYPE))
            ids = [r['id'] for r in cur]
            return ids

        finally:
            cur.close()

    @classmethod
    def numRows(cls, con):
        cur = con.cursor()

        try:
            cur.execute("""
                SELECT count(*)
                FROM sileg.designation
                WHERE description = %s
            """, (cls._TYPE,))
            r = cur.fetchone()
            return None if r is None else r ["count"]

        finally:
            cur.close()


class ExtensionDAO(DesignationDAO):

    _TYPE = 'extension'

    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT id
                FROM sileg.designation
                WHERE description == %s
            """, (cls._TYPE))
            ids = [r['id'] for r in cur]
            return ids

        finally:
            cur.close()

    @classmethod
    def numRows(cls, con):
        cur = con.cursor()

        try:
            cur.execute("""
                SELECT count(*)
                FROM sileg.designation
                WHERE description = %s
            """, (cls._TYPE,))
            r = cur.fetchone()
            return None if r is None else r ["count"]

        finally:
            cur.close()


class OriginalDesignationDAO(DesignationDAO):

    _TYPE = 'original'

    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT id
                FROM sileg.designation
                WHERE description == %s
            """, (cls._TYPE))
            ids = [r['id'] for r in cur]
            return ids

        finally:
            cur.close()

    @classmethod
    def numRows(cls, con):
        cur = con.cursor()

        try:
            cur.execute("""
                SELECT count(*)
                FROM sileg.designation
                WHERE description = %s
            """, (cls._TYPE,))
            r = cur.fetchone()
            return None if r is None else r ["count"]

        finally:
            cur.close()


class Designation(JSONSerializable):

    dao = DesignationDAO

    def __init__(self):
        self.id = None
        self.start = None
        self.end = None
        self.out = None
        self.description = None
        self.userId = None
        self.placeId = None
        self.positionId = None
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
    def findAllHistory(cls, con):
        return cls.dao.findAllHistory(con)

    """
        este método se usa para chequear contra las tablas del sileg y nuestro modelo
        para ver si ya esta creada o no una entidad y no generarla de nuevo
    """
    @classmethod
    def findByUnique(cls, con, oldId, oldType):
        return cls.dao.findByUnique(con, oldId, oldType)

    @classmethod
    def numRows(cls, conn):
        return cls.dao.numRows(conn)


class OriginalDesignation(Designation):
    dao = OriginalDesignationDAO

    def __init__(self):
        super().__init__()
        self.description = self.dao._TYPE


class Extension(Designation):
    dao = ExtensionDAO

    def __init__(self):
        super().__init__()
        self.description = self.dao._TYPE


class Prorogation(Designation):
    dao = ProrogationDAO

    def __init__(self):
        super().__init__()
        self.description = self.dao._TYPE
