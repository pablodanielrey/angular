# -*- coding: utf-8 -*-
import inject, uuid



from model.config import Config
from model.systems.assistance.devices import Devices

class Firmware:

    config = inject.attr(Config)
    devices = inject.attr(Devices)

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
        return self.devices.isEnabled(sid)
