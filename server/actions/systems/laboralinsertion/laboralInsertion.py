# -*- coding: utf-8 -*-
import inject
import base64
import logging
import psycopg2
import uuid
import os
from model.systems.laboralInsertion.laboralInsertion import LaboralInsertion
from model.config import Config
from model.users.users import Users

from zipfile import ZipFile
from collections import OrderedDict
from pyexcel_ods3 import ODSWriter

# from model.exceptions import *

"""
    Modulo de acceso a los datos de insercion laboral
"""

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession


class Utils:

    def __init__(self):
        self.users = inject.instance(Users)

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

        self.serverConfig = inject.instance(Config)
        self.laboralInsertion = inject.instance(LaboralInsertion)
        self.utils = inject.instance(Utils)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.download_async, 'system.laboralInsertion.download')
        yield from self.register(self.find_async, 'system.laboralInsertion.find')
        yield from self.register(self.update_async, 'system.laboralInsertion.update')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def update(self, data):
        con = self._getDatabase()
        try:
            logging.debug('actualizando : {}'.format(data))
            con.commit()
            return True

        finally:
            con.close()

    def find(self, userId):
        con = self._getDatabase()
        try:
            data = self.laboralInsertion.getLaboralInsertionDataByUser(con, userId)
            return data

        finally:
            con.close()

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
            """
            b64 = None
            with open(zipName, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode('utf-8')
            return b64
            """
            return zipName

        except Exception as e:
            logging.exception(e)
            return None

        finally:
            con.close()

    @coroutine
    def download_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.download)
        return r

    @coroutine
    def find_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.find, userId)
        return r

    @coroutine
    def update_async(self, data):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.update, data)
        return r
