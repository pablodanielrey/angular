# -*- coding: utf-8 -*-
import inject
import json
import uuid
import re
import logging
import psycopg2
import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.registry import Registry
from model.connection.connection import Connection
from model.users.users import User, UserPassword
import model.users.users
from model.mail.mail import Mail
from model.ingreso.ingreso import Ingreso


class IngresoWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)
        registry = inject.instance(Registry)
        self.reg = registry.getRegistry('dcsys')
        self.conn = Connection(self.reg)

    @coroutine
    def onJoin(self, details):
        yield from self.register(self.sendEmailConfirmation_async, 'ingreso.mails.sendEmailConfirmation')
        yield from self.register(self.checkEmailCode_async, 'ingreso.mails.checkEmailCode')
        yield from self.register(self.sendErrorMail_async, 'ingreso.mails.sendErrorMail')
        yield from self.register(self.uploadIngresoData_async, 'ingreso.user.uploadIngresoData')
        yield from self.register(self.findByDni_async, 'ingreso.user.findByDni')
        yield from self.register(self.findMails_async, 'ingreso.user.findMails')
        yield from self.register(self.persistMail_async, 'ingreso.user.persistMail')

    def uploadIngresoData(self, dni, password, user, email, eid, code):
        con = self.conn.get()
        try:
            puser = User.findByDni(con, dni)
            if puser is None:
                con.rollback()
                return False

            uid, version = puser
            passwords = UserPassword.findByUserId(con, uid)
            if passwords is None or len(passwords) <= 0:
                passwd = UserPassword()
                passwd.userId = uid
                passwd.username = dni
                passwords = [passwd]
            for passwd in passwords:
                passwd.setPassword(password)
                passwd.persist(con)

            # confirmo el email
            r = Ingreso.confirmEmail(con, eid, code)
            if not r:
                con.rollback()
                return False
            else:
                con.commit()

            # envío el email de finalización
            Ingreso.sendFinalEmail(user, password, email)

            return True

        finally:
            self.conn.put(con)

    @coroutine
    def uploadIngresoData_async(self, dni, password, user, email, eid, code):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.uploadIngresoData, dni, password, user, email, eid, code)
        return r


    def findMails(self, uid):
        con = self.conn.get()
        try:
            mails = model.users.users.Mail.findByUserId(con, uid)
            return mails

        finally:
            self.conn.put(con)

    @coroutine
    def findMails_async(self, uid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findMails, uid)
        return r


    def persistMail(self, omail):
        con = self.conn.get()
        try:
            m = model.users.users.Mail()
            m.userId = omail['user_id']
            m.email = omail['email']
            m.confirmed = False
            mid = m.persist(con)
            con.commit()
            return mid

        finally:
            self.conn.put(con)

    @coroutine
    def persistMail_async(self, omail):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistMail, omail)
        return r


    def findByDni(self, dni):
        con = self.conn.get()
        try:
            u = User.findByDni(con, dni)
            found = False
            if u is not None:
                uid, v = u
                u = User.findById(con, [uid])
                if u is not None and len(u) > 0:
                    found = True

            cursor = con.cursor()
            cursor.execute('insert into ingreso.login (dni, found) values (%s,%s)', (dni, found))
            con.commit()

            if found:
                return u[0]
            else:
                return None

        finally:
            self.conn.put(con)

    @coroutine
    def findByDni_async(self, dni):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findByDni, dni)
        return r

    def sendEmailConfirmation(self, name, lastname, eid):
        con = self.conn.get()
        try:
            logging.warn('sendEmailConfirmation {}'.format(eid))
            Ingreso.sendEmailConfirmation(con, name, lastname, eid)
            con.commit()
            return True

        finally:
            self.conn.put(con)

    @coroutine
    def sendEmailConfirmation_async(self, name, lastname, eid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.sendEmailConfirmation, name, lastname, eid)
        return r

    def checkEmailCode(self, eid, hash):
        con = self.conn.get()
        try:
            r = Ingreso.checkEmailCode(con, eid, hash)
            return r

        finally:
            self.conn.put(con)

    @coroutine
    def checkEmailCode_async(self, eid, hash):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.checkEmailCode, eid, hash)
        return r

    def sendErrorMail(self, error, names, dni, email, comment):
        con = self.conn.get()
        try:
            cursor = con.cursor()
            cursor.execute('insert into ingreso.errors (error, names, dni, email, comment) values (%s,%s,%s,%s,%s)', (error, names, dni, email, comment))
            con.commit()

        finally:
            self.conn.put(con)

        Ingreso.sendErrorEmail(error, names, dni, email, comment)
        return True

    @coroutine
    def sendErrorMail_async(self, error, names, dni, email, tel):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.sendErrorMail, error, names, dni, email, tel)
        return r
