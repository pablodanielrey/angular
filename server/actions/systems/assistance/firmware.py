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

        '''
        yield from self.register(self.deviceAnnounce, 'assistance.server.firmware.deviceAnnounce')
        yield from self.register(self.login_async, 'assistance.server.firmware.syncUser')
        '''

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)


    def deviceAnnounce(self,device):
        pass


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

    def syncUser(self,user,template):
        pass
