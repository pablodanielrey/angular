# -*- coding: utf-8 -*-
import inject
import json
import uuid
import re
import logging
import psycopg2
import hashlib
import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.config import Config
from model.users.users import Users
from model.events import Events
from model.profiles import Profiles
from model.mail.mail import Mail


from model.exceptions import *


class UsersWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        self.users = inject.instance(Users)
        self.serverConfig = inject.instance(Config)
        self.mail = inject.instance(Mail)



    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.findById_async, 'users.findById')
        yield from self.register(self.persistUser_async, 'users.persistUser')
        yield from self.register(self.listUsers_async, 'users.listUsers')
        yield from self.register(self.findUsersIds_async, 'users.findUsersIds')
        yield from self.register(self.findUsersByIds_async, 'users.findUsersByIds')
        yield from self.register(self.findMails_async, 'users.mails.findMails')
        yield from self.register(self.persistMail_async, 'users.mails.persistMail')
        yield from self.register(self.deleteMail_async, 'users.mails.deleteMail')
        yield from self.register(self.sendEmailConfirmation_async, 'users.mails.sendEmailConfirmation')
        yield from self.register(self.confirmEmail_async, 'users.mails.confirmEmail')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def findById(self, id):
        con = self._getDatabase()
        try:
            data = self.users.findUser(con, id)
            return data

        finally:
            con.close()

    @coroutine
    def findById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findById, id)
        return r


    '''
     ' Persistir usuario
     ' Si el id esta definido se actualiza caso contrario se inserta
     ' @param user Diccionario con los datos de usuario
     '    dni
     '    name
     '    lastname
     '    city
     '    country
     '    adress
     '    genre
     '    birthdate
     '    residence_city
     '    version
     '''
    def persistUser(self, user):
        con = self._getDatabase()
        try:
            userId = self.users.updateUser(con, user)

            con.commit()
            return userId

        finally:
            con.close()

    @coroutine
    def persistUser_async(self, user):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistUser, user)
        return r


    '''
     ' Listar usuarios
     '''
    def listUsers(self):
        con = self._getDatabase()
        try:
            users = self.users.listUsers(con)
            return users

        finally:
            con.close()

    @coroutine
    def listUsers_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.listUsers)
        return r


    def findUsersIds(self):
        con = self._getDatabase()
        try:
            usersIds = self.users.listUsersIds(con)
            return usersIds

        finally:
            con.close()

    @coroutine
    def findUsersIds_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findUsersIds)
        return r




    def findUsersByIds(self, ids):
        con = self._getDatabase()
        try:
            # codigo
            con.commit()
            return []

        finally:
            con.close()

    @coroutine
    def findUsersByIds_async(self, ids):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findUsersByIds, ids)
        return r



    '''
     ' Buscar mails a partir de un userId
     ' @param userId Uuid de usuario
     '''
    def findMails(self, userId):
        con = self._getDatabase()
        try:
            mails = self.users.listMails(con, userId)
            return mails

        finally:
            con.close()

    @coroutine
    def findMails_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findMails, userId)
        return r


    '''
     ' Persistir email de usuario
     ' @param email Objeto con los datos del email de usuario
     '      userId: Id de usuario
     '      email: Email propiamente dicho
     '      confirmed: Flag para indicar si el email esta confirmado (Defecto False)
     '''
    def persistMail(self, email):
        con = self._getDatabase()
        try:
            emailId = self.users.createMail(con, email)
            con.commit()
            return emailId

        finally:
            con.close()

    @coroutine
    def persistMail_async(self, email):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistMail, email)
        return r



    '''
     ' Eliminacion de email
     ' @override id uuid del email
     '''
    def deleteMail(self, id):
        con = self._getDatabase()
        try:
            self.users.deleteMail(con, email['id'])
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def deleteMail_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.deleteMail, id)
        return r



    '''
     ' Enviar confirmacion por emai
     ' @param email Datos del email
     '      id: Uuid del email
     '      user_id: Uuid del usuario
     '      email: Email propieamente dicho
     '      confirmed: Flag para indicar si el email esta confirmado o no
     '''
    def sendEmailConfirmation(self, email):
        con = self._getDatabase()
        try:
            hash = hashlib.sha1((email['id'] + email['user_id']).encode('utf-8')).hexdigest()
            email['hash'] = hash

            self.users.updateMail(con,email)

            From = self.serverConfig.configs['mail_confirm_mail_from']
            subject = self.serverConfig.configs['mail_confirm_mail_subject']
            To = email['email']
            template = self.serverConfig.configs['mail_confirm_mail_template']

            url = self.serverConfig.configs['mail_confirm_mail_url']
            url = re.sub('###HASH###', hash, url)

            replace = [
                ('###URL###',url)
            ]

            self.mail.sendMail(From,[To],subject,replace,html=template)

            con.commit()

            return True

        finally:
            con.close()

    @coroutine
    def sendEmailConfirmation_async(self, email):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.sendEmailConfirmation, email)
        return r


    '''
     ' Confirmar email. Una vez confirmado se envia un email al usuario
     ' @param hash Hash del email a confirmar
     '''
    def confirmEmail(self, hash):
        con = self._getDatabase()
        try:
            email = self.users.findMailByHash(con, hash)
            email['confirmed'] = True
            email['hash'] = None

            self.users.updateMail(con,email)

            From = self.serverConfig.configs['mail_confirm_mail_from']
            subject = self.serverConfig.configs['mail_confirm_mail_subject']
            To = email['email']
            template = self.serverConfig.configs['mail_confirm_mail_template']

            url = self.serverConfig.configs['mail_mail_confirmed_template']
            url = re.sub('###HASH###', hash, url)

            replace = [
                ('###URL###',url)
            ]

            self.mail.sendMail(From,[To],subject,replace,html=template)

            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def confirmEmail_async(self, hash):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.confirmEmail, hash)
        return r
