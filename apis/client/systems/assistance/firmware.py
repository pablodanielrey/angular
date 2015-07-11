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


    ''' envía un mensaje de actualización del registro de device dentro del server, tomando los datos del archivo de config del firwamre '''
    def firmwareDeviceAnnounce(self,client,callback):
        device = self.getLocalDevice()
        password = self.config.configs['server_password']

        msg = {
            'action':"FirmwareDeviceAnnounce",
            'password':password,
            'request': device
        }

        client.sendMessage(msg,callback)


    '''
        Envía un mensjae de actualización del usuario dentro del servidor
        El sid usado es el respondido en la llamada firmwareDeviceAnnounce
        Se envía la info del usuario
    '''
    def syncUser(self,sid,client,user,templates,callback):

        msg = {
            'action':'FirmwareSyncUser',
            'session':sid,
            'request':{
                'user':user,
                'templates':templates
            }
        }

        client.sendMessage(msg,callback)

    '''
        Se envía un mensaje de actualización de log dentro del servidor.
        el sid usado es el obtenido en la llamada a firmwareDeviceAnnounce
    '''
    def syncLog(self,sid,client,attlog,callback):

        msg = {
            'action':'FirmwareSyncLog',
            'session':sid,
            'request':{
                'attlog':attlog
            }
        }

        client.sendMessage(msg,callback)
