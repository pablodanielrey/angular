# -*- coding: utf-8 -*-
import uuid
from model.dao import DAO
from model.users.users import UserDAO
from model.serializer.utils import JSONSerializable

class Office(JSONSerializable):
    ''' oficina '''

    def __init__(self):
        self.id = None
        self.parent = None
        self.name = None
        self.telephone = None
        self.email = None
        self.users = []
        self.childs = []

    def appendUser(self, userId):
        if self.users is None:
            self.users = [userId]
        elif userId not in self.users:
            self.users.append(userId)

    def persist(self, con):
        return OfficeDAO.persist(con, self)

    @classmethod
    def findAll(cls, con):
        return OfficeDAO.findAll(con)

    @classmethod
    def findById(cls, con, ids):
        assert isinstance(ids,list)
        offices = [ OfficeDAO.findById(con, oi) for oi in ids ]
        return offices

    @classmethod
    def getOfficesByUserRole(cls, con, userId, tree=False, role='autoriza'):
         return OfficeDAO.getOfficesByUserRole(con, userId, tree, role)

    @classmethod
    def getOfficesByUser(cls, con, userId, tree=False):
        return OfficeDAO.getOfficesByUser(con, userId, tree)


    @classmethod
    def getOfficesUsers(cls, con, offices):
        return OfficeDAO.getOfficesUsers(con, offices)

    @classmethod
    def getOffices(cls, con):
        return OfficeDAO.getOffices(con)

    def getAreas(self, con):
        return OfficeDAO.getAreas(con, self.id)


class OfficeDAO(DAO):
    ''' dao de las oficinas '''
    dependencies = [UserDAO]

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
                  email VARCHAR,
                  parent VARCHAR REFERENCES offices.offices (id),
                  area boolean default false,
                  UNIQUE (name, parent)
                );

                CREATE TABLE IF NOT EXISTS offices.offices_users (
                  user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                  office_id VARCHAR REFERENCES offices.offices (id),
                  UNIQUE (user_id, office_id)
                );

                CREATE TABLE IF NOT EXISTS offices.offices_roles (
                    user_id varchar not null references profile.users (id),
                    office_id varchar references offices.offices (id),
                    role varchar not null,
                    send_mail boolean default true,
                    constraint unique_office_roles unique (user_id,office_id,role)
                );

            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        o = Office()
        o.id = r['id']
        o.parent = r['parent']
        o.name = r['name']
        o.telephone = r['telephone']
        o.email = r['email']
        o.area = r['area']
        return o

    @staticmethod
    def findById(con, oid):
        ''' obtiene la oficina que se identifica con un id '''
        assert oid is not None
        cur = con.cursor()
        try:
            cur.execute('select * from offices.offices where id = %s', (oid,))
            if cur.rowcount <= 0:
                return None

            office = OfficeDAO._fromResult(cur.fetchone())
            cur.execute('select user_id from offices.offices_users where office_id = %s', (office.id,))
            office.users = [c['user_id'] for c in cur]

            return office

        finally:
            cur.close()

    @staticmethod
    def findAll(con):
        ''' obtiene todos los ids '''
        cur = con.cursor()
        try:
            cur.execute('select id from offices.offices')
            ids = [o['id'] for o in cur]
            return ids

        finally:
            cur.close()

    @staticmethod
    def getOffices(con):
        ''' obtiene todos los ids '''
        cur = con.cursor()
        try:
            cur.execute('select id from offices.offices where area = false')
            ids = [o['id'] for o in cur]
            return ids

        finally:
            cur.close()

    @staticmethod
    def getAreas(con, oid):
        ''' obtiene todos los ids '''
        cur = con.cursor()
        try:
            cur.execute('select id from offices.offices where area = true and parent = %s', (oid,))
            ids = [o['id'] for o in cur]
            return ids

        finally:
            cur.close()

    '''
        obtiene las oficinas hijas de las oficinas pasadas como parámetro
    '''
    @classmethod
    def _getChildOffices(cls, con, offices):
        if len(offices) <= 0:
            return []

        '''  obtengo todo el arbol de oficinas abajo de las offices '''
        roffices = []
        pids = []
        pids.extend(offices)

        try:
            cur = con.cursor()

            while len(pids) > 0:
                toFollow = []
                toFollow.extend(pids)
                pids = []

                for oId in toFollow:
                    cur.execute('select id from offices.offices where parent = %s',(oId,))
                    if cur.rowcount <= 0:
                        continue

                    for cOff in cur:
                        cId = cOff[0]
                        if cId not in pids:
                            roffices.append(cId)
                            pids.append(cId)
        finally:
            cur.close()

        return roffices

    '''
        retorna los ids de los usuarios que pertenecen a las oficinas pasasdas como parámetro
        offices = lista de ids de oficinas
    '''
    @classmethod
    def getOfficesUsers(cls,con,offices):

        if len(offices) <= 0:
            return []

        users = []
        cur = con.cursor()

        try:
            child = cls._getChildOffices(con,offices)
            for o in child:
                offices.append(o['id'])

            cur.execute('select distinct user_id from offices.offices_users ou where ou.office_id in %s',(tuple(offices),))
            if cur.rowcount <= 0:
                return []

            for u in cur:
                users.append(u[0])

        finally:
            cur.close()

        return users

    '''
        obtiene todas las oficinas a las cuales el usuario pertenece
    '''
    @classmethod
    def getOfficesByUser(cls,con,userId,tree=False):

        cur = con.cursor()
        ids = []
        try:
            cur.execute('select office_id from offices.offices_users where user_id = %s',(userId,))
            if cur.rowcount <= 0:
                return []

            for off in cur:
                oId = off[0]
                ids.append(oId)

            if tree:
                childrens = cls._getChildOffices(con,ids)
                ids.extend(x for x in childrens if x not in offices)
        finally:
            cur.close()

        return ids


    '''
        obtiene todas las oficinas en las cuales el usuario tiene asignado un rol
        si tree=True obtiene todas las hijas también
    '''
    @classmethod
    def getOfficesByUserRole(cls,con,userId,tree=False,role='autoriza'):

        cur = con.cursor()
        ids = []
        try:
            cur.execute('select id from offices.offices o inner join offices.offices_roles ou on o.id = ou.office_id where ou.user_id = %s and ou.role = %s',(userId,role))
            if cur.rowcount <= 0:
                return []

            for off in cur:
                oId = off[0]
                ids.append(oId)

            if tree:
                childrens = cls._getChildOffices(con,ids)
                ids.extend(x for x in childrens if x not in offices)
        finally:
            cur.close()

        return ids

    @staticmethod
    def persist(con, office):
        ''' inserta o actualiza una oficia '''
        cur = con.cursor()
        try:
            if office.id is None:
                office.id = str(uuid.uuid4())
                params = office.__dict__
                cur.execute('insert into offices.offices (id, name, telephone, email, parent) values (%(id)s, %(name)s, %(telephone)s, %(email)s, %(parent)s)', params)
            else:
                params = office.__dict__
                cur.execute('update offices.offices set name = %(name)s, telephone = %(telephone)s, email = %(email)s, parent = %(parent)s where id = %(id)s', params)

            if office.users is None:
                ''' en el caso de que sea = None no todo la lista de usuarios '''
                return office.id

            ''' actualizo los usuarios de la oficina a partir de offices.users '''
            cur.execute('select user_id from offices.offices_users where office_id = %s', (office.id,))
            idsInBase = [r['user_id'] for r in cur]

            ''' elimino los que ya que no pertenecen a la oficina '''
            notInRuntime = [i for i in idsInBase if i not in office.users]
            for u in notInRuntime:
                cur.execute('delete from offices.offices_users where user_id = %s and office_id = %s', (u, office.id))

            ''' inserto las persona que no existan en la oficina '''
            for u in office.users:
                if u not in idsInBase:
                    cur.execute('insert into offices.offices_users (office_id, user_id) values (%s, %s)', (office.id, u))

            return office.id

        finally:
            cur.close()
