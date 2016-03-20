# -*- coding: utf-8 -*-


class Domain:
    ''' usuarios del dominio '''
    def __init__(self):
        self.id = None


class DomainDAO:
    ''' dao de los usuarios del dominio '''

    @staticmethod
    def _fromResult(r):
        d = Domain()
        d.id = r['id']
        return d

    @staticmethod
    def persist(con, domain):
        ''' setea para que el usuario se sincronize con el dominio y correo '''
        assert domain.id is not None
        cur = con.cursor()
        try:
            params = domain.__dict__
            cur.execute('select id from domain.users where id = %s', (domain.id,))
            if cur.rowcount <= 0:
                cur.execute('insert into domain.users (id) values (%(id)s)', params)

            cur.execute('select id from mail.users where id = %s', (domain.id,))
            if cur.rowcount <= 0:
                cur.execute('insert into mail.users (id) values (%(id)s)', params)

        finally:
            cur.close()

    @staticmethod
    def findAll(con):
        ''' Obtiene todos los Domain '''
        cur = con.cursor()
        try:
            cur.execute('select id from domain.users')
            d = [DomainDAO._fromResult(r) for r in cur]
            return d

        finally:
            cur.close()
