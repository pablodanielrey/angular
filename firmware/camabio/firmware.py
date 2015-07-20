# -*- coding: utf-8 -*-
import codecs, logging, uuid
import psycopg2
import inject

import reader
from template import Templates
from sync import Sync

from model.config import Config
from model.session import Session
from model.profiles import Profiles
from model.users.users import Users
from model.credentials.credentials import UserPassword
from model.systems.assistance.devices import Devices
from model.systems.assistance.logs import Logs
from model.systems.assistance.date import Date

class Firmware:

    reader = reader.getReader()
    users = inject.attr(Users)
    config = inject.attr(Config)
    date = inject.attr(Date)
    logs = inject.attr(Logs)
    devices = inject.attr(Devices)
    templates = inject.attr(Templates)
    session = inject.attr(Session)
    profiles = inject.attr(Profiles)
    userPassword = inject.attr(UserPassword)
    sync = inject.attr(Sync)

    def _get_database(self):
        return psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

    def start(self):
        self.reader.start()

    def stop(self):
        self.reader.stop()
        if self.conn:
            self.conn.close()




    def enroll(self, pin, need_first=None, need_second=None, need_third=None, need_release=None, error=None, fatal_error=None):

        (n,t) = self.reader.enroll(need_first,need_second,need_third,need_release,error,fatal_error)
        if n:
            conn = self._get_database()
            try:

                """ se tiene la huella con el id, hay que asignarle el usuario """
                userId = None
                user = self.users.findUserByDni(conn,pin)
                if not user:
                    user = {
                        'dni':pin,
                        'name':'autorgenerado',
                        'lastname':'autogenerado'
                    }
                    userId = self.users.createUser(conn,user)
                else:
                    userId = user['id']

                self.templates.persist(conn,userId,n,t)
                self.sync.addPerson(conn,userId)
                conn.commit()

            finally:
                conn.close()



    ''' genera lo necesario para loguear una persona dentro del firmware '''
    def _identify(self, conn, userId, verifyMode=1):

        ''' creo el log '''
        log = {
            'id':str(uuid.uuid4()),
            'deviceId':self.config.configs['device_id'],
            'userId':userId,
            'verifymode':verifyMode,
            'log': self.date.utcNow()
        }

        self.logs.persist(conn,log)
        self.sync.addLog(conn,log['id'])

        ''' logueo al usuario creandole una sesion '''
        sess = {
            self.config.configs['session_user_id']:userId
        }
        sid = self.session._create(conn,sess)

        roles = None
        if self.profiles._checkAccessWithCon(conn,sid,['ADMIN-ASSISTANCE']):
            roles = 'admin'

        user = self.users.findUser(conn,userId)

        return (log,user,sid,roles)



    ''' llamado cuando se trata de identificar una persona por huella '''
    def identify(self, notifier=None):
        h = self.reader.identify()
        if h:
            conn = self._get_database()
            try:

                userId = self.templates.findUserIdByIndex(conn,h)
                if userId:
                    (log,user,sid,roles) = self._identify(conn,userId)

                    conn.commit()

                    if notifier:
                        notifier._identified(log,user,sid,roles)

                else:
                    logging.critical('{} - huella identificada en el indice {}, pero no se encuentra ningún mapeo con un usuario'.format(self.date.now(),h))
                    if notifier:
                        notifier._error(h)

            finally:
                conn.close()

        else:
            if notifier:
                notifier._identified(None)




    ''' llamado cuando se trata de identificar una persona usando el teclado '''
    def login(self, pin, password, notifier, server):
        conn = self._get_database()
        try:

            creds = {
                'username':pin,
                'password':password
            }
            userData = self.userPassword.findUserPassword(conn,creds)
            if userData is None:
                notifier._identified(server,None)
                return

            (log,user,sid,roles) = self._identify(conn,userData['user_id'],0)
            conn.commit()

        finally:
            conn.close()

        notifier._identified(server,log,user,sid,roles)



    def syncLogs(self):
        conn = self._get_database()
        try:
            self.sync.syncLogs(conn)

        finally:
            conn.close()


    ''' sincroniza los usuarios que tuvieron cambios en la base del firmware '''
    def syncUsers(self):
        conn = self._get_database()
        try:
            self.sync.syncUsers(conn)

        finally:
            conn.close()
