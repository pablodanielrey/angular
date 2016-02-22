# -*- coding: utf-8 -*-
'''
    Implementa todo el codigo relacionado al modelo y las entidades de los usuarios
'''

import logging
import datetime
import uuid
from connection.connection import Connection


class UserPassword:

    def __init__(self):
        self.id = None
        self.userId = None
        self.username = None
        self.password = None


class UserPasswordDAO:

    @staticmethod
    def _fromResult(r):
        up = UserPassword()
        up.id = r['id']
        up.userId = r['user_id']
        up.username = r['username']
        up.password = r['password']
        up.updated = r['updated']
        return up

    @staticmethod
    def findByUsername(con, username):
        '''
            Obtiene los datos de las credenciales de un usuario
            Retorna:
                Una lista con instancias de UserPassword
                En caso de no existir una lista vacía
        '''
        cur = con.cursor()
        try:
            cur.execute('select id, user_id, username, password, updated from credentials.user_password where username = %s', (username,))
            if cur.rowcount <= 0:
                return []
            data = [UserPasswordDAO._fromResult(c) for c in cur]
            return data

        finally:
            cur.close()


    @staticmethod
    def findByUserId(con, userId):
        '''
            Obtiene los datos de las credenciales de un usuario
            Retorna:
                Una lista con instancias de UserPassword
                En caso de no existir una lista vacía
        '''
        cur = con.cursor()
        try:
            cur.execute('select id, user_id, username, password, updated from credentials.user_password where user_id = %s', (userId,))
            if cur.rowcount <= 0:
                return []
            data = [UserPasswordDAO._fromResult(c) for c in cur]
            return data

        finally:
            cur.close()

    @staticmethod
    def persist(con, up):
        '''
            Inserta o actualiza el usuario y clave de una persona
            Precondiciones:
                El usuario debe existir
            Retorna:
                Id de las credenciales
        '''
        assert up.userId is not None
        assert up.username is not None
        assert up.password is not None

        cur = con.cursor()
        try:
            if up.id is None:
                up.id = str(uuid.uuid4())
                params = up.__dict__
                cur.execute('insert into credentials.user_password (id, user_id, username, password, updated) values (%(id)s, %(userId)s, %(username)s, %(password)s, now())', params)
            else:
                params = up.__dict__
                cur.execute('update credentials.user_password set user_id = %(userId)s, username = %(username)s, password = %(password)s, updated = now() where id = %(id)s', params)

            return up.id

        finally:
            cur.close()


class Mail:
    ''' cuenta de email de un usuario '''

    def __init__(self):
        self.id = None
        self.userId = None
        self.email = None
        self.confirmed = False
        self.hash = None
        self.created = None

    def confirm(con, self):
        ''' cambia el estado a confirmado '''
        if self.confirmed:
            return
        self.confirmed = True
        MailDAO.persist(con, self)


class MailDAO:
    ''' dao de las cuentas de email de los usuarios '''

    @staticmethod
    def _fromResult(r):
        m = Mail()
        m.id = r['id']
        m.userId = r['user_id']
        m.email = r['email']
        m.confirmed = r['confirmed']
        m.hash = r['hash']
        m.created = r['created']
        return m

    @staticmethod
    def findAll(con, userId):
        ''' Obtiene los emails de un usuario '''
        cur = con.cursor()
        try:
            cur.execute('select id, user_id, email, confirmed, hash, created from profile.mails where user_id = %s', (userId,))
            m = [MailDAO._fromResult(ma) for ma in cur]
            return m

        finally:
            cur.close()

    @staticmethod
    def persist(con, mail):
        ''' crea o actualiza un email de usuario '''
        cur = con.cursor()
        try:
            if mail.id is None:
                mail.id = str(uuid.uuid4())
                params = mail.__dict__
                cur.execute('insert into profile.mails (id, user_id, email, confirmed, hash) values (%(id)s, %(userId)s, %(email)s, %(confirmed)s, %(hash)s)', params)
            else:
                params = mail.__dict__
                cur.execute('update profile.mails set user_id = %(userId)s, email = %(email)s, confirmed = %(confirmed)s, hash = %(hash)s where id = %(id)s', params)

        finally:
            cur.close()


class User:
    ''' usuario básico del sistema '''

    def __init__(self):
        self.id = None
        self.dni = None
        self.name = None
        self.lastname = None
        self.genre = None
        self.birthdate = None
        self.city = None
        self.country = None
        self.address = None
        self.residence_city = None
        self.created = datetime.datetime.now()
        self.version = 0
        self.photo = None


class UserDAO:
    ''' DAO para los usuarios '''

    @staticmethod
    def _fromResult(r):
        u = User()
        u.id = r['id']
        u.dni = r['dni']
        u.name = r['name']
        u.lastname = r['lastname']
        u.genre = r['genre']
        u.birthdate = r['birthdate']
        u.city = r['city']
        u.country = r['country']
        u.address = r['address']
        u.residence_city = r['residence_city']
        u.created = r['created']
        u.version = r['version']
        u.photo = r['photo']
        return u

    @staticmethod
    def findAll(con):
        '''
            Obtiene todos los usuarios
            Retorna:
                una lista de tuplas (id, version)
        '''
        cur = con.cursor()
        try:
            cur.execute('select id, version from profile.users')
            users = [(u[0], u[1]) for u in cur]
            return users
        finally:
            cur.close()

    @staticmethod
    def findById(con, uid):
        '''
            Obtiene el usuario especificado por el id
            Retorna:
                User a partir de los datos de la base
                None en caso de que no exista
        '''
        assert uid is not None
        cur = con.cursor()
        try:
            cur.execute('select * from profile.users where id = %s', (uid,))
            if cur.rowcount <= 0:
                return None
            user = UserDAO._fromResult(cur.fetchone())
            return user

        finally:
            cur.close()

    @staticmethod
    def findVersion(con, userId):
        '''
            Obtiene la versión del usuario
            Retorna:
                la version del usuario
                None en caso de que el usuario no exista
        '''
        cur = con.cursor()
        try:
            cur.execute('select version from profile.users where id = %s', (userId,))
            if cur.rowcount > 0:
                return cur.fetchone()[0]
            else:
                return None
        finally:
            cur.close()

    @staticmethod
    def findByDni(con, dni):
        '''
            Obtiene los datos básicos del usuario
            Retorna:
                (id, version)
                None en caso de no existir
        '''
        cur = con.cursor()
        try:
            cur.execute('select id, version from profile.users where dni = %s', (dni,))
            if cur.rowcount <= 0:
                return None
            else:
                (id, version) = cur.fetchone()
                return (id, version)

        finally:
            cur.close()

    @staticmethod
    def persist(con, user):
        '''
            Agrega o actualiza un usuario dentro de la base de datos
        '''
        cur = con.cursor()
        try:
            if user.id is None:
                user.id = str(uuid.uuid4())
                user.version = 0
                cur.execute('insert into profile.users (id, dni, name, lastname, genre, birthdate, city, country, address, residence_city, version, photo) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (
                    user.id,
                    user.dni, user.name, user.lastname,
                    user.genre,
                    user.birthdate,
                    user.city, user.country, user.address, user.residence_city,
                    user.version,
                    user.photo
                ))
                return user.id

            cur.execute('select version from profile.users where id = %s', (user.id,))
            if cur.rowcount <= 0:
                ''' el usuario no existe asi que lo creo '''
                cur.execute('insert into profile.users (id, dni, name, lastname, genre, birthdate, city, country, address, residence_city, version, photo) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (
                    user.id,
                    user.dni, user.name, user.lastname,
                    user.genre,
                    user.birthdate,
                    user.city, user.country, user.address, user.residence_city,
                    user.version,
                    user.photo
                ))
                return user.id
            else:
                ''' el usuario existe asi que chequeo el número de version y si esta ok lo actualizo '''
                v = cur.fetchone()
                if v[0] <= user.version:
                    user.version = user.version + 1
                    params = user.__dict__
                    cur.execute('update profile.users set dni = %(dni)s, name = %(name)s, lastname = %(lastname)s, genre = %(genre)s, ' +
                                'birthdate = %(birthdate)s, ' +
                                'city = %(city)s, country = %(country)s, address = %(address)s, residence_city = %(residence_city)s, ' +
                                'version = %(version)s, ' +
                                'photo = %(photo)s ' +
                                'where id = %(id)s', params)
                    return user.id
                else:
                    raise Exception('versión inferior')

        finally:
            cur.close()


class StudentDAO:

    @staticmethod
    def findAll(con):
        '''
            Obtiene todos los ids de los estudiantes
            Retorno:
                una lista con los ids
        '''
        cur = con.cursor()
        try:
            cur.execute('select id from students.users')
            st = [s[0] for s in cur]
            return st

        finally:
            cur.close()

    @staticmethod
    def findById(con, sId):
        cur = con.cursor()
        try:
            cur.execute('select id, student_number, condition from students.users where id = %s', (sId,))
            if cur.rowcount <= 0:
                return None
            else:
                st = Student()
                st._fromDict(cur.fetchone())
                return st

        finally:
            cur.close()

    @staticmethod
    def persist(con, student):
        '''
            Inserta o actualiza un alumno dentro de la base de datos
            Precondiciones:
                La persona debe existir dentro de la base con el mismo id pasado dentro de student.id
            Retorno:
                El id del estudiante
        '''
        assert student.id is not None
        params = student.__dict__

        cur = con.cursor()
        try:
            cur.execute('select id from students.users where id = %s', (student.id,))
            if cur.rowcount <= 0:
                ''' inserto el alumno dentro de la base de datos '''
                cur.execute('insert into students.users (id, student_number, condition) values (%(id)s, %(studentNumber)s, %(condition)s)', params)
                return student.id
            else:
                cur.execute('update students.users set student_number = %(studentNumber)s, condition = %(condition)s where id = %(id)s', params)
                return student.id

        finally:
            cur.close()


class Student:

    def __init__(self):
        self.id = None
        self.studentNumber = None
        self.condition = None

    def persist(self, con):
        StudentDAO.persist(con, self)

    def _fromDict(self, d):
        self.id = d['id']
        self.studentNumber = d['student_number']
        self.condition = d['condition']


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)
    import sys

    conn = inject.instance(Connection)
    con = conn.getConnection()

    dni = sys.argv[1]
    assert dni is not None

    uid = None

    u = UserDAO.findByDni(con, dni)
    if u is None:
        u = User()
        u.dni = dni
        u.name = sys.argv[2]
        u.lastname = sys.argv[3]
        uid = UserDAO.persist(con, u)
    else:
        (id, version) = u
        uid = id

    s = Student()
    s.id = uid
    s.studentNumber = sys.argv[4]
    s.condition = 'Regular'

    StudentDAO.persist(con, s)
    st = StudentDAO.findById(con, s.id)
    logging.info(st.__dict__)

    passw = UserPasswordDAO.findByUserId(con, uid)
    if passw is None:
        up = UserPassword()
        up.userId = uid
        up.username = dni
        up.password = s.studentNumber
        UserPasswordDAO.persist(con, up)

    passw = UserPasswordDAO.findByUserId(con, uid)
    for p in passw:
        logging.info(p.__dict__)

    con.commit()
    conn.put(con)
