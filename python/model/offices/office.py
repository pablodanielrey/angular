# -*- coding: utf-8 -*-
from model.serializer import JSONSerializable
from model.dao import DAO
from model.users.users import UserDAO, User
from model.offices.designation import Designation

import datetime

import re
import uuid

class Office(JSONSerializable):

    officeType = [{'value': 'office', 'name':'Organigrama'}, {'value': 'unit', 'name': 'Dependencia'}, {'value': 'physical-office', 'name': 'Oficina'}, {'value': 'area', 'name': 'Area'}]

    def __init__(self):
        self.id = None
        self.name = None
        self.telephone = None
        self.number = None
        self.type = None
        self.email = None
        self.parent = None
        self.public = None

    def persist(self, con):
        return OfficeDAO.persist(con, self)

    def remove(self, con):
        return OfficeDAO.remove(con, self.id)

    def findDesignations(self, con):
        pass

    def findChilds(self, con):
        pass

    @classmethod
    def getTypes(cls):
        return cls.officeType

    @classmethod
    def findAll(cls, con, type=None):
        return OfficeDAO.findAll(con, type)

    @classmethod
    def findByIds(cls, con, ids):
        return OfficeDAO.findByIds(con, ids)


class OfficeDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS offices;

                CREATE TABLE IF NOT EXISTS offices.offices (
                  id VARCHAR NOT NULL PRIMARY KEY,
                  name VARCHAR NOT NULL,
                  telephone VARCHAR,
                  nro VARCHAR,
                  email VARCHAR,
                  parent VARCHAR REFERENCES offices.offices (id),
                  type VARCHAR NOT NULL,
                  removed TIMESTAMPTZ,
                  UNIQUE (name)
                );

            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        o = Office()
        o.id = r['id']
        o.name = r['name']
        o.telephone = r['telephone']
        o.number = r['nro']
        o.type = None if r['type'] is None else [t for t in Office.officeType if t['value'] == r['type']][0]
        o.email = r['email']
        o.parent = r['parent']
        o.public = r['public']
        return o

    @classmethod
    def findByIds(cls, con, ids):
        assert ids is not None
        cur = con.cursor()
        try:
            cur.execute('select * from offices.offices where id in %s', (tuple(ids),))
            if cur.rowcount <= 0:
                return []

            return [OfficeDAO._fromResult(o) for o in cur.fetchall()]

        finally:
            cur.close()

    @classmethod
    def findAll(cls, con, types=None):
        cur = con.cursor()
        try:
            if types is None:
                cur.execute('select id from offices.offices where removed is null')
                return [o['id'] for o in cur]
            else:
                assert isinstance(types, list)
                t = [o['value'] for o in types]
                cur.execute('select id from offices.offices where removed is null and type in %s',(tuple(t),))
                return [o['id'] for o in cur]

        finally:
            cur.close()

    @classmethod
    def persist(cls, con, office):
        ''' inserta o actualiza una oficia '''
        cur = con.cursor()
        try:
            if office.id is None:
                office.id = str(uuid.uuid4())
                params = office.__dict__
                cur.execute('insert into offices.offices (id, name, telephone, nro, type, parent, email, public) values (%(id)s, %(name)s, %(telephone)s, %(number)s, %(type)s, %(parent)s, %(email)s, %(public)s)', params)
            else:
                params = office.__dict__
                cur.execute('update offices.offices set name = %(name)s, telephone = %(telephone)s, nro = %(number)s, type = %(type)s, parent = %(parent)s, email = %(email)s, public = %(public)s where id = %(id)s', params)

            return office.id

        finally:
            cur.close()


    @classmethod
    def remove(cls, con, id):
        cur = con.cursor()
        try:
            cur.execute('update offices.offices set removed = NOW() where id = %s', (id,))
            return id
        finally:
            cur.close()


class OfficeModel():

    cache = {}

    """
    @classmethod
    def getOfficesByUser(cls, con, userId, tree=False, types=None):
        idsD = Designation.getDesignationByUser(con, userId)
        desig = Designation.findByIds(con, idsD)
        oIds = [d.officeId for d in desig]
        if types is None:
            return oIds

        offices = Office.findByIds(con, oIds)
        return [office.id for office in offices if office.type in types]
    """

    @classmethod
    def persistDesignations(cls, con, oid, userIds):
        """
            creo las designaciones para una oficina.
            hay que ver cuales ya existían ya que no se deben tocar las fechas de estas designaciones.
        """
        assert oid is not None
        assert isinstance(userIds, list)

        eids = Designation.findByOffice(con, oid, history=False)
        existent = Designation.findByIds(con, eids)

        if len(userIds) <= 0:
            """ elimino todas las deisgnaciones """
            for d in existent:
                d.expire(con)
            return

        toRemove = [d for d in existent if d.userId not in userIds]

        """ elimno las designaciones que no deberían existir """
        for d in toRemove:
            d.expire(con)

        remaining = set(existent) - set(toRemove)
        remainingUsers = [d.userId for d in remaining]
        toGenerate = [u for u in userIds if u not in remainingUsers]

        """ genero y persisto las designaciones adicionales """
        for uid in toGenerate:
            d = Designation()
            d.id = str(uuid.uuid4())
            d.officeId = oid
            d.userId = uid
            d.start = datetime.datetime.now()
            d.persist(con)




    @classmethod
    def getUsers(cls, con, oId):
        idsD = Designation.findByOffice(con, oId)
        desig = Designation.findByIds(con, idsD)
        uIds = set()
        uIds.update([d.userId for d in desig])
        return list(uIds)

    @classmethod
    def searchUsers(cls, con, regex):
        assert regex is not None

        if regex == '':
            return []

        userIds = User.findAll(con)

        users = []
        for u in userIds:
            (uid, version) = u
            if uid not in cls.cache.keys():
                print(uid)
                user = User.findById(con, [uid])[0]
                cls.cache[uid] = user
            users.append(cls.cache[uid])

        m = re.compile(".*{}.*".format(regex), re.I)
        matched = []

        digits = re.compile('^\d+$')
        if digits.match(regex):
            ''' busco por dni '''
            matched = [ cls._getUserData(con, u) for u in users if m.search(u.dni) ]
            return matched

        ''' busco por nombre y apellido '''
        matched = [ cls._getUserData(con, u) for u in users if m.search(u.name) or m.search(u.lastname) or m.search(u.name + u.lastname) or m.search(u.lastname + u.name)]
        return matched

    @classmethod
    def findUsersByIds(cls, con, uids):
        users = User.findById(con, uids)
        return [cls._getUserData(con, u) for u in users]

    @classmethod
    def _getUserData(cls, con, user):
        u = UserIssueData()
        u.name = user.name
        u.lastname = user.lastname
        u.dni = user.dni
        u.id = user.id
        u.genre = user.genre
        u.photo = [User.findPhoto(con, user.photo) if 'photo' in dir(user) and user.photo is not None and user.photo != '' else None][0]
        return u

class UserIssueData(JSONSerializable):

    def __init__(self):
        self.name = ''
        self.lastname = ''
        self.dni = ''
        self.photo = ''
        self.id = ''
