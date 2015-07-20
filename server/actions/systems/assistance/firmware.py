# -*- coding: utf-8 -*-
import inject, logging
import psycopg2

from model.config import Config
from model.systems.assistance.firmware import Firmware

'''
query :
{
  id:,
  action:"FirmwareDeviceAnnounce",
  password:,            --- clave compartida leida desde la config
  request:{
    id:'',
    device:'',
    ip:'',
    enabled:'',
    timezone:''
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    sid:''                --- id de sesion para comunicarse con la api del sistema en los demas métodos
  }

}
'''

class FirmwareDeviceAnnounce:

    firmware = inject.attr(Firmware)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if message['action'] != 'FirmwareDeviceAnnounce':
            return False

        if 'password' not in message:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        request = message['request']
        if ('id' not in request) or ('device' not in request) or ('ip' not in request) or ('timezone' not in request):
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        password = message['password']

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            sid = self.firmware.firmwareDeviceAnnounce(con,password,request)
            if sid is None:
                response = {'id':message['id'], 'error':'Clave de acceso incorrecta'}
                server.sendMessage(response)
                return True

            con.commit()

            response = {
                'id':message['id'],
                'ok':'',
                'response': {
                    'sid':sid
                }
            }
            server.sendMessage(response)
            return True


        except Exception as e:
            logging.exception(e)
            response = {'id':message['id'], 'error':'Excepción'}

        finally:
            con.close()





'''
query :
{
  id:,
 'action':'FirmwareSyncUser',
 'session':sid,
 'request':{
     'user':user,
     'templates':templates
 }
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor"
}
'''

class FirmwareSyncUser:

    firmware = inject.attr(Firmware)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if message['action'] != 'FirmwareSyncUser':
            return False

        if 'session' not in message:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        request = message['request']

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            if not self.firmware.checkSid(con,message['session']):
                response = {'id':message['id'], 'error':'Session de acceso incorrecta'}
                server.sendMessage(response)
                return True

            user = request['user']
            templates = request['templates']
            self.firmware.syncUser(con,user,templates)

            con.commit()

            response = {
                'id':message['id'],
                'ok':''
            }
            server.sendMessage(response)
            return True


        except Exception as e:
            logging.exception(e)
            response = {'id':message['id'], 'error':'Excepción'}

        finally:
            con.close()





'''
query :
{
  id:,
 'action':'FirmwareSyncLogs',
 'session':sid,
 'request':{
     'attlogs': [ attlog ]
 }
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor"
}
'''

class FirmwareSyncLogs:

    firmware = inject.attr(Firmware)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if message['action'] != 'FirmwareSyncLogs':
            return False

        if 'session' not in message:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        request = message['request']

        if 'attlogs' not in request:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True


        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            if not self.firmware.checkSid(con,message['session']):
                response = {'id':message['id'], 'error':'Session de acceso incorrecta'}
                server.sendMessage(response)
                return True


            logs = request['attlogs']
            self.firmware.syncLogs(con,logs)

            con.commit()

            response = {
                'id':message['id'],
                'ok':''
            }
            server.sendMessage(response)
            return True


        except Exception as e:
            logging.exception(e)
            response = {'id':message['id'], 'error':'Excepción'}

        finally:
            con.close()
