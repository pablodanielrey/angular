# -*- coding: utf-8 -*-

import inject, logging

from model.config import Config
from model.users.users import Users
from model.systems.assistance.templates import Templates
from model.systems.assistance.logs  import Logs

class Sync:

    users = inject.attr(Users)
    logs = inject.attr(Logs)
    templates = inject.attr(Templates)

    def addPerson(self,conn,id):
        cur = conn.cursor()
        cur.execute('insert into assistance.sync_user (user_id) values (%s)',(id,))

    def addLog(self,conn,id):
        cur = conn.cursor()
        cur.execute('insert into assistance.sync_logs (attlog_id) values (%s)',(id,))


    def _removeSynchedLogs(self,con,logs):
        cur = con.cursor()
        cur.execute('delete from assistance.sync_logs where attlog_id in %s',(tuple(logs),))


    def _getLogsToSync(self,conn):
        cur = conn.cursor()
        cur.execute('select attlog_id from assistance.sync_logs')
        if cur.rowcount < 0:
            logging.info('No existe log a sincronizar')
            return []

        toSync = []
        for l in cur:
            logId = l[0]
            log = self.logs.findLog(conn,logId)
            if log:
                toSync.append(log)

        if len(toSync) <= 0:
            logging.info('No existe log a sincronizar')
            return []

        return toSync





    ''' se ha sincronizado el usuario en el server, se elimina de la lista a sincronizar '''
    def syncChangedUsersEventHandler(self,con,event):
        user = event['data']['user']
        cur = con.cursor()
        cur.execute('delete from assistance.sync_user where user_id = %s',(user,))


    ''' el servidor envia un los datos de un usuario para ser sincronizado '''
    def syncServerUserEventHandler(self,con,event):
        user = event['data']['user']
        creds = event['data']['credentials']

        if user:
            if self.users.needSync(conn,user):
                self.users.updateUser(conn,user)

        if creds:
            if self.credentials.findCredentials(con,creds['username']) is None:
                self.credentials.createUserPassword(con,creds)
            else:
                self.credentials.updateUserPassword(con,creds)




    ''' envía al servidor los usuarios cuyo id esta dentro de assistance.sync_user '''
    def syncChangedUsers(self,protocol,conn):

        cur = conn.cursor()
        cur.execute('select user_id from assistance.sync_user')
        if cur.rowcount < 0:
            logging.info('No existe usuario a sincronizar')
            return

        toSync = []
        for u in cur:
            userId = u[0]
            user = self.users.findUser(conn,userId)
            if user:
                templates = self.templates.findByUser(conn,userId)
                toSync.append({
                    'user':user,
                    'templates':templates
                })

        if len(toSync) <= 0:
            return

        logging.debug('iniciando sincronización para los usuarios {}'.format(toSync))
        firmware = inject.instance(client.systems.assistance.firmware.Firmware)

        def callbackSync(protocol,message):
            if 'ok' in message:
                logging.debug('OK : '.format(message))
            else:
                logging.debug('ERROR : '.format(message))


        def callbackAnnounce(protocol,message):
            logging.debug('callbackAnnounce {}'.format(message))

            if 'error' in message:
                logging.error('ERROR en announce : {}'.format(message))
                return

            sid = message['response']['sid']
            logging.debug('sincronizando {} con el sid {}'.format(toSync,sid))

            for u in toSync:
                firmware.syncUser(protocol,sid,u['user'],u['templates'],callbackSync)

        def callbackConnect(protocol):
            firmware.firmwareDeviceAnnounce(protocol,callbackAnnounce)

        protocol.addCallback(callbackConnect)





from asyncio import sleep
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

import psycopg2

class WampSync(ApplicationSession):

    delay = 10

    def __init__(self,config=None):
        ApplicationSession.__init__(self, config)

        self.sync = inject.instance(Sync)
        self.firmwareConfig = inject.instance(Config)


    def _getDatabase(self):
        host = self.firmwareConfig.configs['database_host']
        dbname = self.firmwareConfig.configs['database_database']
        user = self.firmwareConfig.configs['database_user']
        passw = self.firmwareConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)


    @coroutine
    def onJoin(self, details):
        logging.debug('WampSync synchronizing')

        conn = self._getDatabase()
        try:
            while True:
                try:
                    logging.debug('Obteniendo los logs a sincronizar')
                    logs = self.sync._getLogsToSync(conn)

                    if len(logs) > 0:
                        logging.debug('Enviando al servidor logs {} a sincronizar'.format(logs))
                        synchedLogs = yield from self.call('assistance.server.firmware.syncLogs',logs)
                        logging.debug('Se sincronizaron {} logs'.format(synchedLogs))

                        if logs:
                            ids = [l['id'] for l in logs]
                            logging.debug('Eliminando logs del sincronizador {}'.format(ids))
                            self.sync._removeSynchedLogs(conn,ids)
                            conn.commit()

                except Exception as e:
                    logging.exception(e)

                try:
                    yield from sleep(self.delay)

                except Exception as e:
                    logging.exception(e)

        finally:
            conn.close()
