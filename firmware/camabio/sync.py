# -*- coding: utf-8 -*-

import inject, logging
from model.users.users import Users
from model.systems.assistance.templates import Templates

import client.network.websocket
from client.systems.assistance.firmware import Firmware

class Sync:

    users = inject.attr(Users)
    templates = inject.attr(Templates)

    def addPerson(self,conn,id):
        cur = conn.cursor()
        cur.execute('insert into assistance.sync_user (user_id) values (%s)',(id,))

    def addLog(self,conn,id):
        cur = conn.cursor()
        cur.execute('insert into assistance.sync_logs (attlog_id) values (%s)',(id,))

    def syncUsers(self,conn):

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


        client.network.websocket.getProtocol().addCallback(callbackConnect)
        client.network.websocket.connectClient()