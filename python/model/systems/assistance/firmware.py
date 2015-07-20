# -*- coding: utf-8 -*-
import inject, uuid



from model.config import Config
from model.users.users import Users
from model.systems.assistance.devices import Devices
from model.systems.assistance.templates import Templates
from model.systems.assistance.logs import Logs


class Firmware:

    config = inject.attr(Config)
    devices = inject.attr(Devices)
    users = inject.attr(Users)
    logs = inject.attr(Logs)
    templates = inject.attr(Templates)

    def __init__(self):
        self.passwords = []
        self._loadPasswordsFromConfig()


    def _loadPasswordsFromConfig(self):
        i = 1
        self.passwords = []
        while True:
            p = 'firmware_password{}'.format(i)
            i = i + 1
            if p in self.config.configs:
                self.passwords.append(self.config.configs[p])
            else:
                break


    def firmwareDeviceAnnounce(self,conn,password,device):
        if password not in self.passwords:
            return None

        self.devices.persistOrUpdate(conn,device)
        return device['id']


    def checkSid(self,conn,sid):
        return self.devices.isEnabled(conn,sid)


    ''' sincroniza los logs enviados como parámetro que no existen en la base '''
    def syncLogs(self,conn,logs):
        if logs is None or len(logs) <= 0:
            return
        self.logs.persistLogs(conn,logs)


    ''' actualiza los datos de los usuarios que tienen versión mayor a la del usuario en la base '''
    def syncUser(self,conn,user,templates):
        if self.users.needSync(conn,user):
            self.users.updateUser(conn,user)

        if templates is not None:
            for t in templates:
                if self.templates.needSync(conn,t):
                    self.templates.update(conn,t)
