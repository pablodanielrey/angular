# -*- coding: utf-8 -*-
import uuid


class Office:
    ''' oficina '''

    def __init__(self):
        self.id = None
        self.parent = None
        self.name = None
        self.telephone = None
        self.email = None
        self.users = None


class OfficeDAO:
    ''' dao de las oficinas '''

    @staticmethod
    def _fromResult(r):
        o = Office()
        o.id = r['id']
        o.parent = r['parent']
        o.name = r['name']
        o.telephone = r['telephone']
        o.email = r['email']
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


class Group:
    ''' Grupo de usuarios '''

    def __init__(self):
        pass
