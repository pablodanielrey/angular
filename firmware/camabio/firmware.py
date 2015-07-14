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

    def __init__(self):
        self.conn = None

    def __get_database(self):
        if self.conn:
            return self.conn
        else:
            return psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

    def start(self):
        self.reader.start()

    def stop(self):
        self.reader.stop()
        if self.conn:
            self.conn.close()




    def enroll(self, pin, need_first=None, need_second=None, need_third=None, need_release=None):

        (n,t) = self.reader.enroll(need_first,need_second,need_third,need_release)
        if n:
            self.conn = self.__get_database()

            """ se tiene la huella con el id, hay que asignarle el usuario """
            userId = None
            user = self.users.findUserByDni(self.conn,pin)
            if not user:
                user = {
                    'dni':pin,
                    'name':'autorgenerado',
                    'lastname':'autogenerado'
                }
                userId = self.users.createUser(self.conn,user)
            else:
                userId = user['id']

            self.templates.persist(self.conn,userId,n,t)
            self.sync.addPerson(self.conn,userId)
            self.conn.commit()




    ''' genera lo necesario para loguear una persona dentro del firmware '''
    def _identify(self, userId, verifyMode=1):

        ''' creo el log '''
        log = {
            'id':str(uuid.uuid4()),
            'deviceId':self.config.configs['device_id'],
            'userId':userId,
            'verifymode':verifyMode,
            'log': self.date.utcNow()
        }
        self.logs.persist(self.conn,log)
        self.sync.addLog(self.conn,log['id'])

        ''' logueo al usuario creandole una sesion '''
        sess = {
            self.config.configs['session_user_id']:userId
        }
        sid = self.session._create(self.conn,sess)

        roles = None
        if self.profiles._checkAccessWithCon(self.conn,sid,['ADMIN-ASSISTANCE']):
            roles = 'admin'

        user = self.users.findUser(self.conn,userId)

        return (log,user,sid,roles)



    ''' llamado cuando se trata de identificar una persona por huella '''
    def identify(self, notifier=None):
        h = self.reader.identify()
        if h:
            self.conn = self.__get_database()

            userId = self.templates.findUserIdByIndex(self.conn,h)
            if userId:
                (log,user,sid,roles) = self._identify(userId)

                self.conn.commit()

                if notifier:
                    notifier._identified(log,user,sid,roles)

            else:
                logging.critical('{} - huella identificada en el indice {}, pero no se encuentra ningún mapeo con un usuario'.format(self.date.now(),h))
                if notifier:
                    notifier._error(h)

        else:
            if notifier:
                notifier._identified(None)




    ''' llamado cuando se trata de identificar una persona usando el teclado '''
    def login(self, pin, password, notifier, server):
        self.conn = self.__get_database()

        creds = {
            'username':pin,
            'password':password
        }
        userData = self.userPassword.findUserPassword(self.conn,creds)
        if userData is None:
            notifier._identified(server,None)
            return

        (log,user,sid,roles) = self._identify(userData['user_id'],0)

        self.conn.commit()

        notifier._identified(server,log,user,sid,roles)



    ''' sincroniza los usuarios que tuvieron cambios en la base del firmware '''
    def syncUsers(self):

        self.conn = self.__get_database()
        self.sync.syncUsers(self.conn)
