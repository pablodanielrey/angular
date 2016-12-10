import uuid
import logging
import datetime
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

class GAuth:

    #SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
    #SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
    #          'https://www.googleapis.com/auth/drive']

    @classmethod
    def getCredentials(cls, scopes, username):
            home_dir = os.path.expanduser('~')
            credential_dir = os.path.join(home_dir, '.credentials')
            if not os.path.exists(credential_dir):
                os.makedirs(credential_dir)
            credential_path = os.path.join(credential_dir,'credentials.json')

            credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path, scopes)

            ''' cuenta de admin '''
            admin_credentials = credentials.create_delegated(username)

            return admin_credentials

    @classmethod
    def getService(cls, service, version, scopes, username):
        credentials = cls.getCredentials(scopes, username)
        http = credentials.authorize(httplib2.Http())
        service = discovery.build(service, version, http=http)
        return service

SCOPE = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/spreadsheets'
]

if __name__ == '__main__':

    guser = sys.argv[1]

    gmail = GAuth.getService('gmail','v1', SCOPE, guser)
    print(gmail.users().labels().list(userId='me').execute())
