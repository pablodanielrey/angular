# -*- coding: utf-8 -*-
import inject

from model.config import Config

class Firmware:

    config = inject.attr(Config)

    def __init__(self):
        self.sid = None

    ''' setea el sid para usar en los métodos que necesiten acceso al server '''
    def setSID(self,sid):
        self.sid = sid


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
    def syncUser(self,protocol,user,templates,callback):

        msg = {
            'action':'FirmwareSyncUser',
            'session':self.sid,
            'request':{
                'user':user,
                'templates':templates
            }
        }

        protocol.sendMessage(msg,callback)

    '''
        Se envía un mensaje de actualización de log dentro del servidor.
        el sid usado es el obtenido en la llamada a firmwareDeviceAnnounce
    '''
    def syncLog(self,protocol,attlog,callback):

        msg = {
            'action':'FirmwareSyncLog',
            'session':self.sid,
            'request':{
                'attlog':attlog
            }
        }

        protocol.sendMessage(msg,callback)
