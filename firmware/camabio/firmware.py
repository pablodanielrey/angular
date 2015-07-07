# -*- coding: utf-8 -*-
import codecs, logging, uuid
import psycopg2
import inject

import reader
from template import Templates

from model.config import Config
from model.session import Session
from model.profiles import Profiles
from model.users.users import Users
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
            self.conn.commit()


    def identify(self, notifier=None):
        logging.debug('reader.identify')
        h = self.reader.identify()
        logging.debug('reader identify = {}'.format(h))
        if h:
            self.conn = self.__get_database()

            userId = self.templates.findUserIdByIndex(self.conn,h)
            if userId:

                ''' creo el log '''
                log = {
                    'id':str(uuid.uuid4()),
                    'deviceId':self.config.configs['device_id'],
                    'userId':userId,
                    'verifymode':1,
                    'log': self.date.utcNow()
                }
                self.logs.persist(self.conn,log)

                ''' logueo al usuario creandole una sesion '''
                sess = {
                    self.config.configs['session_user_id']:userId
                }
                sid = self.session._create(self.conn,sess)

                self.conn.commit()

                roles = None
                if self.profiles._checkAccessWithCon(self.conn,sid,['ADMIN-ASSISTANCE']):
                    roles = 'admin'


                user = self.users.findUser(self.conn,userId)
                logging.debug('log {} persona {}'.format(log,user))

                if notifier:
                    notifier._identified(log,user,sid,roles)

            else:
                logging.critical('{} - huella identificada en el indice {}, pero no se encuentra ningún mapeo con un usuario'.format(self.date.now(),h))
                if notifier:
                    notifier._error(h)

        else:
            if notifier:
                notifier._identified(None)
