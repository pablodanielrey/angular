# -*- coding: utf-8 -*-
from model.serializer import JSONSerializable
from model.dao import DAO
from model.users.users import UserDAO, User
import re

class Office(JSONSerializable):

    officeType = [{'value': 'office', 'name':'Organigrama'}, {'value': 'unit', 'name': 'Dependencia'}, {'value': 'physical-office', 'name': 'Oficina'}, {'value': 'area', 'name': 'Area'}]

    def __init__(self):
        self.id = None
        self.name = None
        self.telephone = None
        self.number = None
        self.type = self.officeType[1]
        self.email = None
        self.parent = None

    def persist(self, con):
        return OfficeDAO.persist(con, self)

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
        o.type = [t for t in Office.officeType if t['value'] == r['type']][0]
        o.email = r['email']
        o.parent = r['parent']
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
    def findAll(cls, con, types=Office.officeType):
        cur = con.cursor()
        try:
            if len(types) < 1 or (len(types) == 1 and types[0]['value'] is None):
                types = Office.officeType

            t = [o['value'] for o in types]
            cur.execute('select id from offices.offices where type in %s',(tuple(t),))
            return [o['id'] for o in cur]

        finally:
            cur.close()

    @classmethod
    def persit(cls, con, off):
        return


class Designation(JSONSerializable):

    def __init__(self):
        self.id = None
        self.officeId = None
        self.position = 'Cumple función'
        self.userId = None
        self.start = None
        self.end = None

    @classmethod
    def removeByIds(cls, con, ids):
        DesignationDAO.removeByIds(con, ids)

    def remove(self, con):
        DesignationDAO.removeByIds(con, [self.id])

    @classmethod
    def findByIds(cls, con, ids):
        return DesignationDAO.findByIds(con, ids)

    @classmethod
    def getDesignationByUser(cls, con, userId, history=False):
        return DesignationDAO.getDesignationByUser(con, userId, history)

    @classmethod
    def getDesignationByOffice(cls, con, officeId, history=False):
        return DesignationDAO.getDesignationByOffice(con, officeId, history)

    @classmethod
    def getDesignationByPosition(cls, con, position, history=False):
        return DesignationDAO.getDesignationByPosition(con, position, history)

    def persist(self, con):
        return DesignationDAO.persist(con, self)



class DesignationDAO(DAO):
    dependencies = [UserDAO, OfficeDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS offices;

                CREATE TABLE IF NOT EXISTS offices.designation (
                  id VARCHAR PRIMARY KEY,
                  user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                  office_id VARCHAR REFERENCES offices.offices (id),
                  position VARCHAR,
                  sstart DATE default now(),
                  send DATE,
                  UNIQUE (user_id, office_id, position)
                );
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        d = Designation()
        d.id = r['id']
        d.officeId = r['office_id']
        d.position = r['position']
        d.userId = r['user_id']
        d.start = r['sstart']
        d.end = r['send']
        return d

    @classmethod
    def removeByIds(cls, con, ids):
        assert ids is not None
        cur = con.cursor()
        try:
            cur.execute('delete from offices.designation where id in %s', (ids,))

        finally:
            cur.close()


    @classmethod
    def findByIds(cls, con, ids):
        assert ids is not None
        cur = con.cursor()
        try:
            cur.execute('select * from offices.designation where id in %s order by sstart asc', (ids,))
            if cur.rowcount <= 0:
                return []

            return [DesignationDAO._fromResult(d) for d in cur.fetchall()]

        finally:
            cur.close()

    @classmethod
    def getDesignationByUser(cls, con, userId, history=False):
        assert userId is not None
        cur = con.cursor()
        try:
            if history is None or not history:
                cur.execute('select id from offices.designation where user_id = %s and send is null order by sstart',(userId,))
            else:
                cur.execute('select id from offices.designation where user_id = %s order by sstart',(userId,))

            return [d['id'] for d in cur]

        finally:
            cur.close()

    @classmethod
    def getDesignationByOffice(cls, con, officeId, history=False):
        assert officeId is not None
        cur = con.cursor()
        try:
            if history is None or not history:
                cur.execute('select id from offices.designation where office_id = %s and send is null',(officeId,))
            else:
                cur.execute('select id from offices.designation where office_id = %s',(officeId,))

            return [d['id'] for d in cur]

        finally:
            cur.close()

    @classmethod
    def getDesignationByPosition(cls, con, position, history=False):
        assert position is not None
        cur = con.cursor()
        try:
            if history is None or not history:
                cur.execute('select id from offices.designation where position = %s and send is null',(position,))
            else:
                cur.execute('select id from offices.designation where position = %s',(position,))

            return [d['id'] for d in cur]

        finally:
            cur.close()

    @classmethod
    def persist(cls, con, desig):
        return


class OfficeModel():

    cache = {}

    @classmethod
    def getOfficesByUser(cls, con, userId, tree=False, types=None):
        idsD = Designation.getDesignationByUser(con, userId)
        desig = Designation.findByIds(con, idsD)
        oIds = [d.officeId for d in desig]
        if types is None:
            return oIds

        offices = Office.findByIds(con, oIds)
        return [office.id for office in offices if office.type in types]

    @classmethod
    def getUsers(cls, con, oId):
        idsD = Designation.getDesignationByOffice(con, oId)
        desig = Designation.findByIds(con, idsD)
        uIds = []
        for d in desig:
            if d.userId not in uids:
                uIds.append(d.userId)
        return uIds


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
