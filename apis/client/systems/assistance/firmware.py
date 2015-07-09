# -*- coding: utf-8 -*-
import inject

from model.config import Config

class Firmware:

    config = inject.attr(Config)

    def getLocalDevice(self):
        device = {
            'id': self.config.configs['device_id'],
            'device': self.config.configs['device_name'],
            'ip': self.config.configs['firmware_ip'],
            'enabled': self.config.configs['device_enabled'],
            'timezone': self.config.configs['device_timezone']
        }
        return device


    def firmwareDeviceAnnounce(self,client,callback):
        device = self.getLocalDevice()
        password = self.config.configs['server_password']

        msg = {
            'action':"FirmwareDeviceAnnounce",
            'password':password,
            'request': device
        }

        client.sendMessage(msg,callback)
