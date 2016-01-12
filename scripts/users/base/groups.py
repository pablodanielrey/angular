# -*- coding: utf-8 -*-


class Office:
    ''' oficina '''

    def __init__(self):
        self.id = None
        self.parent = None
        self.name = None
        self.telephone = None
        self.email = None
        self.users = []


class OfficeDAO:
    ''' dao de las oficinas '''

    @staticmethod
    def findAll(con):
        ''' obtiene todos los ids '''

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
                cur.execute('update offices.offices (name, telephone, email, parent) values (%(name)s, %(telephone)s, %(email)s, %(parent)s)', params)

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
