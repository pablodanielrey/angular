from actions.systems.assistance.export import ExportModelBase
from model.assistance.utils import Utils

import uuid
import logging
import datetime
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
    def getCredentials(cls, username):
            home_dir = os.path.expanduser('~')
            credential_dir = os.path.join(home_dir, '.credentials')
            if not os.path.exists(credential_dir):
                os.makedirs(credential_dir)
            credential_path = os.path.join(credential_dir,'credentials.json')

            credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path, cls.SCOPES)

            ''' uso una cuenta de admin del dominio '''
            admin_credentials = credentials.create_delegated(username)

            return admin_credentials

    @classmethod
    def getService(cls, username):
        credentials = cls.getCredentials(username)
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

            pip3 install google-api-python-client google-oauth

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
    def _getDate(cls, date):
        pass

    @classmethod
    def _getTime(cls, date):
        pass

    @classmethod
    def createSpreadsheet(cls, service, spId):
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
        return r['spreadsheetId']

    @classmethod
    def exportLogs(cls, ownerId, logs, usersData):
        classfiedUsersData = cls.classifyUserData(usersData)
        justifications = {}

        spId = str(uuid.uuid4())
        service = GAuthSheets.getService('{}@econo.unlp.edu.ar'.format(ownerId))
        spId = cls.createSpreadsheet(service, spId)

        ''' actualizo los logs '''
        rows = []
        for log in logs:
            user = classfiedUsersData[log.userId]
            row = [
                user.name,
                user.lastname,
                user.dni,
                log.verifyMode,
                str(log.log.date()) if log.log is not None else '',
                str(log.log.time()) if log.log is not None else ''
            ]
            rows.append(row)

        valueRange = {
            'majorDimension': cls.majorDimension['rows'],
            'values': rows
        }

        service.spreadsheets().values().append(spreadsheetId=spId,
                        range='A1',
                        valueInputOption=cls.inputOption['user'],
                        body=valueRange).execute()
        return spId

    @classmethod
    def exportStatistics(cls, ownerId, stats, usersData):
        classfiedUsersData = cls.classifyUserData(usersData)
        justifications = {}

        spId = str(uuid.uuid4())
        service = GAuthSheets.getService('{}@econo.unlp.edu.ar'.format(ownerId))
        spId = cls.createSpreadsheet(service, spId)

        ''' actualizo los logs '''
        rows = []
        for stat in stats:
            user = classfiedUsersData[stat.userId]
            row = [
                user.name,
                user.lastname,
                user.dni,
                stat.position,
                str(stat.scheduleStart.date()) if stat.scheduleStart is not None else '',
                str(stat.scheduleStart.time()) if stat.scheduleStart is not None else '',
                str(stat.scheduleEnd.date()) if stat.scheduleEnd is not None else '',
                str(stat.scheduleEnd.time()) if stat.scheduleEnd is not None else '',
                str(stat.logStart.date()) if stat.logStart is not None else '',
                str(stat.logStart.time()) if stat.logStart is not None else '',
                str(stat.logEnd.date()) if stat.logEnd is not None else '',
                str(stat.logEnd.time()) if stat.logEnd is not None else '',
                str(datetime.timedelta(seconds=stat.workedSeconds))
            ]
            rows.append(row)

        valueRange = {
            'majorDimension': cls.majorDimension['rows'],
            'values': rows
        }

        service.spreadsheets().values().append(spreadsheetId=spId,
                        range='A1',
                        valueInputOption=cls.inputOption['user'],
                        body=valueRange).execute()
        return spId
