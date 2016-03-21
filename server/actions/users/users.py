# -*- coding: utf-8 -*-
import inject
import logging
import uuid
import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.users.users import UserDAO, User, Telephone, MailDAO
from model.tutorias.tutorias import TutoriasModel
from model.registry import Registry
from model.connection import connection
from model.mail.mail import Mail
# from model.exceptions import *


class UsersWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        reg = inject.instance(Registry)
        self.conn = connection.Connection(reg.getRegistry('dcsys'))
        self.tutoriasModel = inject.instance(TutoriasModel)
        self.mails = inject.instance(MailDAO)
        self.mail = inject.instance(Mail)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.findById_async, 'users.findById')
        yield from self.register(self.findByDni_async, 'users.findByDni')
        yield from self.register(self.persistUser_async, 'users.persistUser')
        yield from self.register(self.listUsers_async, 'users.listUsers')
        yield from self.register(self.findUsersIds_async, 'users.findUsersIds')
        yield from self.register(self.findUsersByIds_async, 'users.findUsersByIds')
        yield from self.register(self.findMails_async, 'users.mails.findMails')
        yield from self.register(self.persistMail_async, 'users.mails.persistMail')
        yield from self.register(self.deleteMail_async, 'users.mails.deleteMail')
        yield from self.register(self.sendEmailConfirmation_async, 'users.mails.sendEmailConfirmation')
        yield from self.register(self.confirmEmail_async, 'users.mails.confirmEmail')

        yield from self.register(self.search_async, 'users.search')

    def search(self, regex):
        con = self.conn.get()
        try:
            users = self.tutoriasModel.search(con, regex)
            return users

        finally:
            self.conn.put(con)

    @coroutine
    def search_async(self, regex):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.search, regex)
        return r

    def findById(self, id):
        con = self.conn.get()
        try:
            data = UserDAO.findById(con, id)
            if data is None:
                return None
            ru = data.__dict__
            ru['telephones'] = [ t.__dict__ for t in data.telephones ]
            return ru
        finally:
            self.conn.put(con)

    @coroutine
    def findById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findById, id)
        return r

    def findByDni(self, dni):
        con = self.conn.get()
        try:
            data = UserDAO.findByDni(con, dni)
            return data

        finally:
            self.conn.put(con)

    @coroutine
    def findByDni_async(self, dni):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findByDni, dni)
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
        con = self.conn.get()
        try:
            telephones = user['telephones']

            u = User()
            u.__dict__ = user
            u.telephones = []
            for t in telephones:
                logging.info(t)
                t2 = Telephone()
                t2.__dict__ = t
                u.telephones.append(t2)
                logging.info(u.telephones)
            userId = UserDAO.persist(con, u)
            con.commit()
            return userId

        finally:
            self.conn.put(con)

    @coroutine
    def persistUser_async(self, user):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistUser, user)
        return r

    '''
     ' Listar usuarios
     '''
    def listUsers(self):
        con = self.conn.get()
        try:
            users = UserDAO.listUsers(con)
            return users

        finally:
            self.conn.put(con)

    @coroutine
    def listUsers_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.listUsers)
        return r

    def findUsersIds(self):
        con = self.conn.get()
        try:
            usersIds = UserDAO.listUsersIds(con)
            return usersIds

        finally:
            self.conn.put(con)

    @coroutine
    def findUsersIds_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findUsersIds)
        return r

    def findUsersByIds(self, ids):
        con = self.conn.get()
        try:
            usersIds = UserDAO.findUsersByIds(con, ids)
            return usersIds

        finally:
            self.conn.put(con)

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
        con = self.conn.get()
        try:
            mails = self.mails.findByUserId(con, userId)
            return [ m.__dict__ for m in mails ]

        finally:
            self.conn.put(con)

    @coroutine
    def findMails_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findMails, userId)
        return r

    '''
     ' Persistir email de usuario
     ' @param email Objeto con los datos del email de usuario
     '      user_id: Id de usuario
     '      email: Email propiamente dicho
     '      confirmed: Flag para indicar si el email esta confirmado (Defecto False)
     '''
    def persistMail(self, email):
        con = self.conn.get()
        try:
            emailId = UserDAO.createMail(con, email)
            con.commit()
            return emailId

        finally:
            self.conn.put(con)

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
        con = self.conn.get()
        try:
            UserDAO.deleteMail(con, id)
            con.commit()
            return True

        finally:
            self.conn.put(con)

    @coroutine
    def deleteMail_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.deleteMail, id)
        return r

    '''
     ' Enviar confirmacion por emai
     ' @param emailId Uuid del email
     '''
    def sendEmailConfirmation(self, emailId):
        con = self.conn.get()
        try:
            UserDAO.sendEmailConfirmation(con, emailId)
            con.commit()
            return True

        finally:
            self.conn.put(con)

    @coroutine
    def sendEmailConfirmation_async(self, emailId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.sendEmailConfirmation, emailId)
        return r

    '''
     ' Confirmar email. Una vez confirmado se envia un email al usuario
     ' @param hash Hash del email a confirmar
     '''
    def confirmEmail(self, hash):
        con = self.conn.get()
        try:
            UserDAO.confirmEmail(con, hash)
            con.commit()
            return True

        finally:
            self.conn.put(con)

    @coroutine
    def confirmEmail_async(self, hash):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.confirmEmail, hash)
        return r
