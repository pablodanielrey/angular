# -*- coding: utf-8 -*-
import inject, logging
import psycopg2

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config
from model.systems.assistance.firmware import Firmware


'''
    Clase que da acceso mediante wamp a los métodos del firmware
'''
class WampFirmware(ApplicationSession):

    def __init__(self,config=None):
        logging.debug('instanciando WampFirmware')
        ApplicationSession.__init__(self, config)

        self.firmware = inject.instance(Firmware)
        self.serverConfig = inject.instance(Config)


    '''
    como referencia tambien se puede sobreeescribir el onConnect
    def onConnect(self):
        logging.debug('transport connected')
        self.join(self.config.realm)
    '''

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.syncLogs_async, 'assistance.server.firmware.syncLogs')
        yield from self.register(self.syncUser_async, 'assistance.server.firmware.syncUser')

        '''
        yield from self.register(self.deviceAnnounce, 'assistance.server.firmware.deviceAnnounce')

        '''

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)


    def deviceAnnounce(self,device):
        pass


    '''
        Guarda los logs pasados como parámetro dentro de la base de datos.
        retorna:
            lista con los logs que fueron guardados exitósamente y que no existían
    '''
    def syncLogs(self,attlogs):
        con = self._getDatabase()
        try:
            synchedLogs = self.firmware.syncLogs(con,attlogs)
            con.commit()
            return synchedLogs

        finally:
            con.close()

    @coroutine
    def syncLogs_async(self,attlogs):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None,self.syncLogs,attlogs)
        return r


    '''
        Actualiza la información del usuario y sus templates dentro de la base de datos
    '''
    def syncUser(self,user,templates):
        con = self._getDatabase()
        try:
            self.firmware.syncUser(con,user,templates)
            con.commit()

        finally:
            con.close()

    @coroutine
    def syncUser_async(self,user,templates):
        try:
            loop = asyncio.get_event_loop()
            yield from loop.run_in_executor(None,self.syncUser,user,templates)
            return user['id']

        except Exception as e:
            logging.exception(e)
            return None
