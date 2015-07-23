# -*- coding: utf-8 -*-

import inject, logging
from model.users.users import Users
from model.systems.assistance.templates import Templates
from model.systems.assistance.logs  import Logs

import client.network.websocket
from client.systems.assistance.firmware import Firmware

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


    def syncLogEventHandler(self,con,event):
        logs = event['data']['logs']

        cur = con.cursor()
        cur.execute('delete from assistance.sync_logs where attlog_id in %s',(tuple(logs),))



    def syncLogs(self,protocol,conn):
        cur = conn.cursor()
        cur.execute('select attlog_id from assistance.sync_logs')
        if cur.rowcount < 0:
            logging.info('No existe log a sincronizar')
            return

        toSync = []
        for l in cur:
            logId = l[0]
            log = self.logs.findLog(conn,logId)
            if log:
                toSync.append(log)

        if len(toSync) <= 0:
            logging.info('No existe log a sincronizar')
            return

        logging.debug('iniciando sincronización de los logs {}'.format(toSync))
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

            firmware.syncLogs(protocol,sid,toSync,callbackSync)

        def callbackConnect(protocol):
            firmware.firmwareDeviceAnnounce(protocol,callbackAnnounce)

        protocol.addCallback(callbackConnect)




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
