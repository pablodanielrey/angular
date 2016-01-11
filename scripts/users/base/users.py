# -*- coding: utf-8 -*-
'''
    Implementa todo el codigo relacionado al modelo y las entidades de los usuarios
'''
import psycopg2
from psycopg2 import pool
import logging
import datetime
import uuid

logging.getLogger().setLevel(logging.INFO)

pool = psycopg2.pool.ThreadedConnectionPool(10, 20, host='163.10.17.80', database='dcsys', user='dcsys', password='dcsys')


def getConnection():
    global pool
    return pool.getconn()


def closeConnection(con):
    global pool
    pool.putconn(con)


class UserPassword:

    def __init__(self):
        self.id = None
        self.userId = None
        self.username = None
        self.password = None

    @staticmethod
    def _fromResult(r):
        up = UserPassword()
        up.id = r[0]
        up.userId = r[1]
        up.username = r[2]
        up.password = r[3]
        return up


class UserPasswordDAO:

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
            cur.execute('select id, user_id, username, password from credentials.user_password where user_id = %s', (userId,))
            if cur.rowcount <= 0:
                return []
            data = [UserPassword._fromResult(c) for c in cur]
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
                cur.execute('insert into credentials.user_password (id, user_id, username, password) values (%(id)s, %(userId)s, %(username)s, %(password)s)', params)
            else:
                params = up.__dict__
                cur.execute('update credentials.user_password set user_id = %(userId)s, username = %(username)s, password = %(password)s where id = %(id)s', params)

            return up.id

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
                    cur.execute('update profile.users set ' +
                                'dni = %s, name = %s, lastname = %s, ' +
                                'genre = %s, ' +
                                'birthdate = %s, ' +
                                'city = %s, country = %s, address = %s, residence_city = %s, ' +
                                'version = %s, ' +
                                'photo = %s',
                                (user.id,
                                 user.dni, user.name, user.lastname,
                                 user.genre,
                                 user.birthdate,
                                 user.city, user.country, user.address, user.residence_city,
                                 user.version,
                                 user.photo
                                 ))
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
        self.id = d[0]
        self.studentNumber = d[1]
        self.condition = d[2]


if __name__ == '__main__':

    import sys

    con = getConnection()

    dni = sys.argv[1]
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
    closeConnection(con)
