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
        if self.profiles._checkUserProfile(conn,userId,['ADMIN-ASSISTANCE']):
            roles = 'admin'

        user = self.users.findUser(conn,userId)

        return (log,user,sid,roles)



    ''' llamado cuando se trata de identificar una persona por huella '''
    def identify(self):
        h = self.reader.identify()
        if h:
            conn = self._get_database()
            try:
                userId = self.templates.findUserIdByIndex(conn,h)
                if userId:
                    data = self._identify(conn,userId)
                    conn.commit()
                    return data

                else:
                    logging.critical('{} - huella identificada en el indice {}, pero no se encuentra ningún mapeo con un usuario'.format(self.date.now(),h))
                    return None

            except Exception as e:
                logging.exception(e)
                raise e

            finally:
                conn.close()

        else:
            return None




    ''' llamado cuando se trata de identificar una persona usando el teclado '''
    def login(self, pin, password):
        conn = self._get_database()
        try:
            creds = {
                'username':pin,
                'password':password
            }
            userData = self.userPassword.findUserPassword(conn,creds)
            if userData is None:
                return None

            data = self._identify(conn,userData['user_id'],0)
            conn.commit()

            return data

        except Exception as e:
            logging.exception(e)
            raise e

        finally:
            conn.close()







    ''' retorna un handler para manejar los eventos de sincronizacion '''
    def syncLogEventHandler(self):
        def eventHandler(event):

            if 'LogsSynchedEvent' != event['type']:
                return


            conn = self._get_database()
            try:
                self.sync.syncLogEventHandler(conn,event)
                conn.commit()

            except Exception as e:
                logging.exception(e)

            finally:
                conn.close()

        return eventHandler


    ''' inicia el proceso de sincronización de los logs hacia el server '''
    def syncLogs(self,protocol):
        conn = self._get_database()
        try:
            self.sync.syncLogs(protocol,conn)

        finally:
            conn.close()


    ''' retorna un hanlder para manejar los eventos de sincronización de los usuarios '''
    def syncChangedUsersEventHandler(self):
        def eventHandler(event):

            if 'UserSynchedEvent' != event['type']:
                return

            conn = self._get_database()
            try:
                self.sync.syncChangedUsersEventHandler(conn,event)
                conn.commit()

            except Exception as e:
                logging.exception(e)

            finally:
                conn.close()

        return eventHandler


    ''' retorna un hanlder para manejar los eventos de sincronización de los ususuarios enviados por el servidor '''
    def syncUsersEventHandler(self):
        def eventHandler(event):

            if 'SynchUserEvent' != event['type']:
                return

            conn = self._get_database()
            try:
                self.sync.syncServerUserEventHandler(conn,event)
                conn.commit()

            except Exception as e:
                logging.exception(e)

            finally:
                conn.close()

        return eventHandler



    ''' sincroniza los usuarios que tuvieron cambios en la base del firmware '''
    def syncChangedUsers(self,protocol):
        conn = self._get_database()
        try:
            self.sync.syncChangedUsers(protocol,conn)

        finally:
            conn.close()
