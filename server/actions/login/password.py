# -*- coding: utf-8 -*-
import psycopg2, logging
import inject
import hashlib
import re

from model.profiles import Profiles
from model.mail.mail import Mail
from model.config import Config
from model.events import Events
from model.users.users import Users
from model.credentials.credentials import UserPassword
from model.session import Session, SessionNotFound

from model.exceptions import *


"""
peticion:
{
    id: "id de la peticion"
    action: "changePassword"
    username: 'nombre de usuario'
    password: 'clave a configurar'
    session: "id de session, en caso de cambiar la clave a un usuario logueado"
    hash: "hash generado, en caso de cambiar la clave a un usuario NO logueado (resetPassword)"
}

respuesta:
{
    id: "id de la peticion",
    ok: 'mensaje de ok, en caso correcto del cambio'
    error: 'mensaje de error en caso de error en el cambio'
}
"""

class ChangePassword:

    profiles = inject.attr(Profiles)
    userPassword = inject.attr(UserPassword)
    session = inject.attr(Session)
    config = inject.attr(Config)


    def changePassword(self, con, sid, username, password):
        s = self.session.getSession(sid)
        user_id = s[self.config.configs['session_user_id']]
        creds = self.userPassword.findCredentials(con, username)

        if (creds['user_id'] != user_id):
            ''' se esta tratando de modificar credenciales que pertenecen a otro usuario, no el de la session indicada '''
            if not self.profiles.checkAccess(sid, 'ADMIN'):
                raise InsuficientAccess()

        newCreds = {
            'id': creds['id'],
            'user_id': creds['user_id'],
            'username': username,
            'password': password
        }
        self.userPassword.updateUserPassword(con,newCreds);



    def handleAction(self, server, message):

        if 'id' not in message:
            raise MalformedMessage()

        if 'action' not in message:
            raise MalformedMessage()

        if message['action'] != 'changePassword':
            return False

        if 'username' not in message:
            raise MalformedMessage()

        username = message['username']
        password = message['password']


        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            ''' es un reseteo de clave? '''
            if 'hash' in message:

                hash = message['hash']
                self.userPassword.resetUserPassword(con,hash,username,password)

                response = {'id':message['id'], 'ok':'se ha cambiado la clave exitósamente'}
                server.sendMessage(response)

                con.commit()

                return True

            """ es un cambio normal de un usuario logueado """
            """ chequeo que exista la sesion, etc """
            sid = message['session']
            self.profiles.checkAccess(sid,['ADMIN','USER'])

            self.changePassword(con,sid,username,password)

            con.commit()

            response = {'id':message['id'], 'ok':'se ha cambiado la clave exitósamente'}
            server.sendMessage(response)

            return True

        finally:
            con.close()


"""
peticion:
{
    id: "id de la peticion"
    action: "resetPassword"
    username: 'nombre de usuario'
}

respuesta:
{
    id: "id de la peticion",
    ok: 'mensaje de ok, en caso correcto de la generación y envio por correo.'
    error: 'mensaje de error en caso de error'
}
"""


class ResetPassword:

    users = inject.attr(Users)
    userPassword = inject.attr(UserPassword)
    mail = inject.attr(Mail)
    config = inject.attr(Config)


    ''' envío el hash a todos los mails que tenga confirmado el usuario '''
    def sendEmail(self, con, hash, username):

        """
            variables a reemplazar :
            ###DNI###
            ###NAME###
            ###LASTNAME###
            ###URL###

            y estas en a url.
            ###HASH###
            ###USERNAME###
        """


        creds = self.userPassword.findCredentials(con,username)
        user_id = creds['user_id']
        user = self.users.findUser(con,user_id)
        mails = self.users.listMails(con,user_id)
        emails = [x['email'] for x in mails if x['confirmed'] == True]

        if len(emails) <= 0:
            raise FailedConstraints('No tienen ningún email confirmado')

        url = self.config.configs['mail_reset_password_url']
        url = re.sub('###HASH###', hash, url)
        url = re.sub('###USERNAME###', username, url)

        From = self.config.configs['mail_reset_password_from']
        subject = self.config.configs['mail_reset_password_subject']
        template = self.config.configs['mail_reset_password_template']

        replace = [
            ('###DNI###',user['dni']),
            ('###NAME###',user['name']),
            ('###LASTNAME###',user['lastname']),
            ('###URL###',url)
        ]

        self.mail.sendMail(From,emails,subject,replace,html=template)

        return True



    def handleAction(self, server, message):

        if 'id' not in message:
            raise MalformedMessage()

        if 'action' not in message:
            raise MalformedMessage()

        if message['action'] != 'resetPassword':
            return False

        if 'username' not in message:
            raise MalformedMessage()

        username = message['username']

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            hash = self.userPassword.getResetPasswordHash(con,username)
            self.sendEmail(con, hash, username)

            con.commit()

            response = {'id':message['id'], 'ok':'hash generado correctamente'}
            server.sendMessage(response)

            return True

        finally:
            con.close()
