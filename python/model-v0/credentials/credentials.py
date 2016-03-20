# -*- coding: utf-8 -*-
import uuid, hashlib, psycopg2

from model.exceptions import *
from model.objectView import ObjectView

"""

datos de la entidad

{
    username:''
    password:''
    user_id:''
    id:''
}

"""


class UserPassword:

    ''' cambia la clave de un usuario siempre y cuando se haya generado el hash previo usado getResetPasswordHash '''
    def resetUserPassword(self, con, hash, username, password):
        cur = con.cursor()
        cur.execute('select creds_id, user_id from credentials.password_resets where executed = false and hash = %s and username = %s', (hash, username))
        d = cur.fetchone()
        if d is None:
            raise UserNotFound()

        newCreds = {
            'id': d[0],
            'user_id': d[1],
            'username': username,
            'password': password
        }
        self.updateUserPassword(con, newCreds)
        cur.execute('update credentials.password_resets set executed = true where hash = %s and username = %s', (hash, username))

    ''' genera el hash necesario para resetear la clave de un usuario '''
    def getResetPasswordHash(self, con, username):
        creds = self.findCredentials(con, username)
        if creds is None:
            raise UserNotFound()

        try:
            hash = hashlib.sha1((str(uuid.uuid4()) + username).encode('utf-8')).hexdigest()

            rreq = (creds['id'], creds['user_id'], creds['username'], hash)
            cur = con.cursor()
            cur.execute('insert into credentials.password_resets (creds_id, user_id, username, hash) values (%s,%s,%s,%s)', rreq)

            return hash

        except psycopg2.DatabaseError as e:
            con.rollback()
            raise e

    """
    {
        user_id:''
        username:''
        password:''
    }
    """
    def createUserPassword(self, con, user):
        try:
            rreq = (str(uuid.uuid4()), user['user_id'], user['username'], user['password'])
            cur = con.cursor()
            cur.execute('insert into credentials.user_password (id,user_id,username,password) values (%s,%s,%s,%s)', rreq)

        except psycopg2.DatabaseError as e:
            raise e

    """
    {
        id: ''
        username: ''
        password: ''
        user_id: ''
    }
    """
    def updateUserPassword(self, con, user):
        try:
            rreq = (user['user_id'], user['username'], user['password'], user['id'])
            cur = con.cursor()
            cur.execute('update credentials.user_password set user_id = %s, username = %s, password = %s, updated = now() where id = %s', rreq)

        except psycopg2.DatabaseError as e:
            raise e

    """
    {
        username: ''
        password: ''
    }
    """
    def findUserPassword(self, con, credentials):
        cred = ObjectView(credentials)
        cur = con.cursor()
        cur.execute('select id, user_id, username from credentials.user_password where username = %s and password = %s', (cred.username, cred.password))
        data = cur.fetchone()
        if data is not None:
            return self.convertToDict(data)
        else:
            return None

    def findCredentials(self, con, username):
        cur = con.cursor()
        cur.execute('select id, user_id, username from credentials.user_password where username = %s', (username,))
        data = cur.fetchone()
        if data is not None:
            return self.convertToDict(data)
        else:
            return None

    ''' transformo a diccionario las respuestas de psycopg2'''
    def convertToDict(self, d):
        rdata = {
            'id': d[0],
            'user_id': d[1],
            'username': d[2]
        }
        return rdata
