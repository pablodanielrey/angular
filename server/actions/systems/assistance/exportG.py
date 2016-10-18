from actions.systems.assistance.export import ExportModelBase
from model.assistance.utils import Utils

import uuid
import logging

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

class GAuthSheets:

    #SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']

    @classmethod
    def getCredentials(cls):
            home_dir = os.path.expanduser('~')
            credential_dir = os.path.join(home_dir, '.credentials')
            if not os.path.exists(credential_dir):
                os.makedirs(credential_dir)
            credential_path = os.path.join(credential_dir,'credentials.json')

            credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path, cls.SCOPES)

            ''' uso una cuenta de admin del dominio '''
            admin_credentials = credentials.create_delegated('27294557@econo.unlp.edu.ar')

            return admin_credentials

    @classmethod
    def getService(cls):
        credentials = cls.getCredentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('sheets', 'v4', http=http)
        return service


class ExportModel(ExportModelBase):
    '''
        Exportación a google spreadsheets.
        hace falta tener instalado:
            apt-get install python3-googleapi
            apt-get install python3-google-apputils python3-googleapi python3-googlecloudapis
            pip3 install google-oauth

        y tener dentro del home del ususario que correo el proceso las credenciales de google para la api.
        dentro de :
            $HOME/.credentials/credentials.json
    '''

    majorDimension = {
        'rows': 'ROWS',
        'cols': 'COLUMS'
    }

    inputOption = {
        'raw': 'RAW',
        'user': 'USER_ENTERED'
    }

    @classmethod
    def exportLogs(cls, logs, usersData):
        classfiedUsersData = cls.classifyUserData(usersData)
        justifications = {}

        spId = str(uuid.uuid4())
        service = GAuthSheets.getService()

        ''' creo la hoja de calculo '''

        logging.info('Creando hoja de calculo {}'.format(spId))
        body = {
            'spreadsheetId': spId,
            'properties': {
                'title': 'Reporte Asistencia Logs',
                'locale':'es_AR'
            }
        }
        r = service.spreadsheets().create(body=body).execute()
        logging.info(r)
        spId = r['spreadsheetId']

        ''' actualizo los logs '''
        i = 1
        for log in logs:
            user = classfiedUsersData[log.userId]
            row = [
                user.name,
                user.lastname,
                user.dni,
                log.verifyMode,
                str(log.log) if log.log is not None else '',
                str(log.log) if log.log is not None else ''
            ]

            valueRange = {
                'majorDimension': cls.majorDimension['rows'],
                'values': [row]
            }

            service.spreadsheets().values().append(spreadsheetId=spId,
                            range='A{}'.format(i),
                            valueInputOption=cls.inputOption['user'],
                            body=valueRange).execute()
            i = i + 1

        return ''

    @classmethod
    def exportStatistics(cls, stats, usersData):
        classfiedUsersData = cls.cls.classifyUserData(usersData)
        return ''
