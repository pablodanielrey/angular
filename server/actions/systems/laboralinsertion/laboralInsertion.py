# -*- coding: utf-8 -*-
import inject
import base64
import logging

import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor

import uuid
import os
from model.laboralinsertion.laboralInsertion import LaboralInsertion
from model.laboralinsertion.inscription import Inscription
from model.laboralinsertion.company import Company, CompanyDAO, Contact
from model.laboralinsertion.languages import Language
from model.laboralinsertion.filters import Filter

import model.laboralinsertion
from model.laboralinsertion.mails import Sent, SentDAO
from model.users.users import UserDAO
from model.users.users import MailDAO
from model.registry import Registry
from model.connection import connection

from zipfile import ZipFile
from collections import OrderedDict

# from model.exceptions import *

"""
    Modulo de acceso a los datos de insercion laboral
"""

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession


class Utils:

    def __init__(self):
        self.users = inject.instance(UserDAO)

    def _prepareCvs(self, cvs):
        b64s = []
        for c in cvs:
            b64 = base64.b64encode(c['cv']).decode('utf-8')
            b64s.append({
                'data': b64,
                'name': c['name'],
                'username': c['username'],
                'lastname': c['lastname']
            })
        return b64s


class LaboralInsertionWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        reg = inject.instance(Registry)
        self.conn = connection.Connection(reg.getRegistry('dcsys'))
        self.laboralInsertion = inject.instance(LaboralInsertion)
        self.utils = inject.instance(Utils)
        self.users = inject.instance(UserDAO)
        self.mails = inject.instance(MailDAO)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.download_async, 'system.laboralInsertion.download')
        yield from self.register(self.findByUser_async, 'system.laboralInsertion.findByUser')
        yield from self.register(self.persist_async, 'system.laboralInsertion.persist')
        yield from self.register(self.findAllInscriptions_async, 'system.laboralInsertion.findAllInscriptions')
        yield from self.register(self.findAllInscriptionsByUser_async, 'system.laboralInsertion.findAllInscriptionsByUser')
        yield from self.register(self.persistInscriptionByUser_async, 'system.laboralInsertion.persistInscriptionByUser')
        yield from self.register(self.deleteInscriptionById_async, 'system.laboralInsertion.deleteInscriptionById')
        yield from self.register(self.sendMailToCompany_async, 'system.laboralInsertion.sendEmailToCompany');
        yield from self.register(self.findSentByInscriptionId_async, 'system.laboralInsertion.sent.findByInscription');
        yield from self.register(self.getFilters_async, 'system.laboralInsertion.getFilters');
        yield from self.register(self.findAllCompanies_async, 'system.laboralInsertion.company.findAll');
        yield from self.register(self.persistCompany_async, 'system.laboralInsertion.company.persist');


    def persist(self, data):
        con = self.conn.get()
        try:
            u = model.laboralinsertion.user.User()
            u.__dict__ = data
            languages = []
            for l in data['languages']:
                l['id'] = l['id'] if 'id' in l else None
                l['userId'] = u.id
                l2 = Language()
                l2.__dict__ = l
                languages.append(l2)

            self.laboralInsertion.persist(con, u, languages)
            con.commit()
            return True

        finally:
            self.conn.put(con)

    def findByUser(self, userId):
        con = self.conn.get()
        try:
            data = self.laboralInsertion.findByUser(con, userId)
            if data is None:
                return None
            """
            eid = data.email
            mails = MailDAO.findById(con, eid)
            if mails is not None and len(mails) > 0:
                data.email = mails[0].__dict__
            else:
                data.email = ''
            """

            user = data.__dict__
            user['languages'] = [ l.__dict__ for l in data.languages ]
            return user

        finally:
            self.conn.put(con)

    def findAllInscriptionsByUser(self, userId):
        con = self.conn.get()
        try:
            data = self.laboralInsertion.findAllInscriptionsByUser(con, userId)
            insc = [ i.__dict__ for i in data ]
            return insc

        finally:
            self.conn.put(con)

    def findAllInscriptions(self, filters):
        con = self.conn.get()
        try:
            filterss = Filter.fromMapList(filters)
            data = self.laboralInsertion.findAllInscriptions(con, filterss)
            insc = [ i.__dict__ for i in data ]
            return insc

        finally:
            self.conn.put(con)

    def getFilters(self):
        con = self.conn.get()
        try:
            data = self.laboralInsertion.getFilters()
            return data

        finally:
            self.conn.put(con)

    def persistInscriptionByUser(self, userId, data):
        con = self.conn.get()
        try:
            """ primero busco que no exista esa misma inscripción """
            inscriptions = self.laboralInsertion.findAllInscriptionsByUser(con, userId)
            ins = [ i for i in inscriptions if i.degree == data['degree'] and i.workType == data['workType'] and not i.deleted ]
            if len(ins) >= 1:
                raise Exception('Ya existe esa inscripcion')

            if 'id' not in data:
                data['id'] = None
            data['userId'] = userId
            i = Inscription()
            i.__dict__ = data

            self.laboralInsertion.persistInscription(con, i)
            con.commit()
            return True

        finally:
            self.conn.put(con)

    def deleteInscriptionById(self, iid):
        con = self.conn.get()
        try:
            self.laboralInsertion.deleteInscriptionById(con, iid)
            con.commit()
            return True

        finally:
            self.conn.put(con)

    def download(self):
        con = self.conn.get()
        try:
            self.laboralInsertion.download(con)
            return True

        finally:
            self.conn.put(con)

    def sendMailToCompany(self, inscriptions, emails, inscriptionsPerMail):
        con = self.conn.get()
        try:
            inscriptionIds = [ i['id'] for i in inscriptions ]
            inscriptionsToSend = [ inscriptionIds.pop() for i in range(inscriptionsPerMail) if len(inscriptionIds) > 0 ]
            data = []
            while len(inscriptionsToSend) > 0:
                data.extend(self.laboralInsertion.sendMailToCompany(con, inscriptionsToSend, emails))
                inscriptionsToSend = [ inscriptionIds.pop() for i in range(inscriptionsPerMail) if len(inscriptionIds) > 0 ]

            self.publish('system.laboralInsertion.COMPANYSENDED', data)
            return True

        finally:
            self.conn.put(con)

    def findAllCompanies(self):
        con = self.conn.get()
        try:
            ids = CompanyDAO.findAll(con)
            return CompanyDAO.findById(con, ids)

        finally:
            self.conn.put(con)

    def persistCompany(self, company):
        con = self.conn.get()
        try:
            id = CompanyDAO.persist(con, company)
            con.commit()
            return id

        finally:
            self.conn.put(con)

    def findSentByInscriptionId(self, id):
        con = self.conn.get()
        try:
            ids = SentDAO.findByInscriptionId(con, id)
            return ids

        finally:
            self.conn.put(con)

    """
    def download(self):
        con = self._getDatabase()
        try:
            path = '{}/tmp'.format(os.getcwd())
            zipName = '{}.zip'.format(str(uuid.uuid4()))
            with ZipFile('{}/{}'.format(path, zipName), 'w') as myzip:
                database = self.laboralInsertion.getLaboralInsertionData(con)
                data = self.utils._arrangeForOds(con, database)
                ods = self.utils._exportToOds(data)
                myzip.write(ods, os.path.basename(ods))

                cvs = self.laboralInsertion.findAllCvs(con)
                for c in cvs:
                    ext = os.path.splitext(c['name'])[1]
                    if ext is None:
                        ext = '.desconocida'

                    filename = '{}/{}, {}{}'.format(path, c['lastname'], c['username'], ext)
                    with open(filename, 'wb') as f:
                        f.write(c['cv'])

                    myzip.write(filename, os.path.basename(filename))

            b64 = None
            with open(zipName, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode('utf-8')
            return b64

            return zipName

        except Exception as e:
            logging.exception(e)
            return None

        finally:
            self._closeDatabase(con)
    """

    @coroutine
    def download_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.download)
        return r

    @coroutine
    def findByUser_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findByUser, userId)
        return r

    @coroutine
    def findAllInscriptions_async(self, filters):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findAllInscriptions, filters)
        return r

    @coroutine
    def getFilters_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getFilters)
        return r

    @coroutine
    def findAllInscriptionsByUser_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findAllInscriptionsByUser, userId)
        return r

    @coroutine
    def persistInscriptionByUser_async(self, userId, data):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistInscriptionByUser, userId, data)
        return r

    @coroutine
    def deleteInscriptionById_async(self, iid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.deleteInscriptionById, iid)
        return r

    @coroutine
    def persist_async(self, data):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persist, data)
        return r

    @coroutine
    def sendMailToCompany_async(self, inscriptions, company, inscriptionsPerMail):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.sendMailToCompany, inscriptions, company, inscriptionsPerMail)
        return r

    @coroutine
    def findAllCompanies_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findAllCompanies)
        return r

    @coroutine
    def persistCompany_async(self, data):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistCompany, data)
        return r

    @coroutine
    def findSentByInscriptionId_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findSentByInscriptionId, id)
        return r
