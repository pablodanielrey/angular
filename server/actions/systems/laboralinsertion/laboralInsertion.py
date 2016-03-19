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
from model.laboralinsertion.company import Company, CompanyDAO
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

    """
    def _exportToOds(self, data):
        ods = OrderedDict()
        ods.update({"Datos": data})
        filename = '/tmp/{}.ods'.format(str(uuid.uuid4()))
        writer = ODSWriter(filename)
        writer.write(ods)
        writer.close()
        return filename

    def _arrangeForOds(self, con, data):
        values = [['Fecha de Inscripción', 'Apellido', 'Nombre', 'Sexo', 'Fecha Nacimiento', 'Edad', 'Dni', 'e-Mail', 'País', 'Ciudad de Origen', 'Ciudad de residencia', 'Legajo', 'Viajar', 'Residir', 'Ingles', 'Portugués', 'Otro', 'Carrera', 'Cantidad de materias', 'Promedio con aplazos', 'Promedio', 'Pasantía', 'Tiempo Completo', 'Jóvenes Profesionales']]
        for l in data:
            v = []

            userId = l['id']
            user = self.users.findUser(con, userId)
            mails = self.users.listMails(con, user['id'])

            v.append(l['creation'].date())

            v.append(user['lastname'])
            v.append(user['name'])
            v.append(user['genre'] if user['genre'] != None else '')
            v.append(user['birthdate'] if user['birthdate'] != None else '')
            v.append('')
            v.append(user['dni'])

            if len(mails) > 0:
                v.append(mails[0]['email'])
            else:
                v.append('')

            v.append('')
            v.append('')
            v.append(user['residence_city'] if user['residence_city'] else '')

            v.append('')

            if l['travel']:
                v.append('Sí')
            else:
                v.append('No')

            if l['reside']:
                v.append('Sí')
            else:
                v.append('No')

            langIng = ''
            langPort = ''
            langOtro = ''
            for la in l['languages']:
                if la['name'] != None and (la['name'].lower() == 'inglés' or la['name'].lower() == 'ingles'):
                    langIng = '{} - {}, '.format(la['name'], la['level'])

                if la['name'] == 'Portugués':
                    langPort = '{} - {}, '.format(la['name'], la['level'])

                langOtro = '{} - {}, '.format(la['name'], la['level'])

            v.append(langIng)
            v.append(langPort)
            v.append(langOtro)

            if len(l['degrees']) > 0:
                for d in l['degrees']:
                    vaux = list(v)
                    vaux.append(d['name'] if d['name'] else '')
                    vaux.append(d['courses'] if d['courses'] else '')
                    vaux.append(d['average2'] if d['average2'] else '')
                    vaux.append(d['average1'] if d['average1'] else '')

                    workType = d['work_type']
                    if 'intership' in workType:
                        vaux.append('Sí')
                    else:
                        vaux.append('No')

                    if 'FullTime' in workType:
                        vaux.append('Sí')
                    else:
                        vaux.append('No')

                    if 'YoungProfessionals' in workType:
                        vaux.append('Sí')
                    else:
                        vaux.append('No')

                    values.append(vaux)
            else:
                v.append('')
                v.append('')
                v.append('')
                v.append('')
                v.append('')
                v.append('')
                v.append('')
                values.append(v)

        return values
    """

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
        yield from self.register(self.findAllCompanies_async, 'system.laboralInsertion.company.findAll');
        yield from self.register(self.findSentByInscriptionId_async, 'system.laboralInsertion.sent.findByInscription');
        yield from self.register(self.getFilters_async, 'system.laboralInsertion.getFilters');


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

    def sendMailToCompany(self, inscriptions, company):
        con = self.conn.get()
        try:
            c = Company()
            c.__dict__ = company
            data = self.laboralInsertion.sendMailToCompany(con, inscriptions, c)
            self.publish('system.laboralInsertion.COMPANYSENDED', data)
            return True

        finally:
            self.conn.put(con)

    def findAllCompanies(self):
        con = self.conn.get()
        try:
            ids = CompanyDAO.findAll(con)
            cs = CompanyDAO.findById(con, ids)
            css = [c.__dict__ for c in cs]
            return css

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
    def sendMailToCompany_async(self, inscriptions, company):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.sendMailToCompany, inscriptions, company)
        return r

    @coroutine
    def findAllCompanies_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findAllCompanies)
        return r

    @coroutine
    def findSentByInscriptionId_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findSentByInscriptionId, id)
        return r
