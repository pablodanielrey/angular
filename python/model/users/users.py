# -*- coding: utf-8 -*-
'''
    Implementa todo el codigo relacionado al modelo y las entidades de los usuarios
'''

import re
import logging
import datetime
import uuid
from model.connection.connection import Connection
from model.serializer import JSONSerializable
from model.dao import DAO
from model.files.files import File, FileDAO








############### Student ###############



############### UserPassword ###############


class UserPasswordDAO(DAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS credentials;

              CREATE TABLE IF NOT EXISTS credentials.user_password(
                id VARCHAR NOT NULL PRIMARY KEY,
                user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                username VARCHAR NOT NULL UNIQUE,
                password VARCHAR NOT NULL,
                updated TIMESTAMP DEFAULT now()
              );
            """


            cur.execute(sql)

        finally:
            cur.close()


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
    def findByUserPassword(con, username, password):
        cur = con.cursor()
        try:
            cur.execute('select * from credentials.user_password where username = %s and password = %s', (username, password))
            if cur.rowcount <= 0:
                return None
            return UserPasswordDAO._fromResult(cur.fetchone())

        finally:
            cur.close()

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
            if not hasattr(up, 'id') or up.id is None:
                up.id = str(uuid.uuid4())
                params = up.__dict__
                cur.execute('insert into credentials.user_password (id, user_id, username, password, updated) values (%(id)s, %(userId)s, %(username)s, %(password)s, now())', params)
            else:
                params = up.__dict__
                cur.execute('update credentials.user_password set user_id = %(userId)s, username = %(username)s, password = %(password)s, updated = now() where id = %(id)s', params)

            return up.id

        finally:
            cur.close()


class UserPassword(JSONSerializable):

    dao = UserPasswordDAO

    def __init__(self):
        self.id = None
        self.userId = None
        self.username = None
        self.password = None

    def setPassword(self, passw):
        self.password = passw

    def persist(self, con):
        self.dao.persist(con, self)

    @classmethod
    def findByUserId(cls, con, userId):
        return cls.dao.findByUserId(con, userId)

    @classmethod
    def findByUsername(cls, con, username):
        return cls.dao.findByUsername(con, username)

    @classmethod
    def findByUserPassword(cls, con, username, password):
        return cls.dao.findByUserPassword(con, username, password)


############### Mail ###############
