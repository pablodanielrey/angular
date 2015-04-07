# -*- coding: utf-8 -*-
import json, base64, datetime, traceback, logging
import inject
import psycopg2

from wexceptions import *

from model.config import Config
from model.profiles import Profiles
from model.events import Events

from model.systems.assistance.assistance import Assistance
from model.systems.assistance.date import Date
from model.systems.assistance.justifications.justifications import Justifications


"""
query : Obtener todas las solicitudes de justificationces
{
  id:,
  action:"getOvertimeRequestsToManage",
  session:,
  request:{
      status: 'estado de la justificacion PENDING|APPROVED|REJECTED|CANCELED' -- si no existe se obtienen todas,
      group: "ROOT|TREE" -- si no existe obtiene las del grupo directo que puede manejar.
  }
}


"""
class GetOvertimeRequestsToManage:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    overtime = inject.attr(Overtime)

    def handleAction(self, server, message):

        if (message['action'] != 'getOvertimeRequestsToManage'):
            return False

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        status = None
        if 'status' in message['request']:
            status = message['request']['status']

        group = None
        if 'group' in message['request']:
            group = message['request']['group']


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            requests = self.overtime.getOvertimeRequestsToManage(con,userId,status,group)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'requests':requests
                }
            }
            server.sendMessage(response)
            return True

        except Exception as e:
            raise e

        finally:
            con.close()



"""

query : Obtener todas las solicitudes de justificationces
{
  id:,
  action:"getOvertimeRequests",
  session:,
  request:{
      status: 'estado de la justificacion PENDING|APPROVED|REJECTED|CANCELED' -- si no existe se obtienen todas,
  }
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    requests : [ "lista de solicitudes"
  		{
	      id: "id de la solicitud de hora extra",
          user_id:"id del usuario para el cual se solicito hora extra",
    	  begin: 2014-12-01 00:00:00 "fecha y hora de inicio de la hora extra"
    	  end: 2014-12-02 00:00:00 "fecha y hora de finalizacion de la hora extra"
    	  reason: "motivo de la solicitud"
    	  status: "PENDING|APPROVED|REJECTED|CANCELED (estado de la solicitud)"
  		}
	]
}

"""
class GetOvertimeRequests:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    overtime = inject.attr(Overtime)

    def handleAction(self, server, message):

        if (message['action'] != 'getOvertimeRequests'):
            return False

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        status = None
        if 'status' in message['request']:
            status = message['request']['status']


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            requests = self.overtime.getOvertimeRequests(con,status,[userId])

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'requests':requests
                }
            }
            server.sendMessage(response)
            return True

        except Exception as e:
            raise e

        finally:
            con.close()




"""
query : solicitud de justificaciones de un determinado usuario
{
  id:,
  action:"updateOvertimeRequestStatus",
  session:,
  request:{
      request_id: "id del pedido",
      status: "PENDING|APPROVED|REJECTED|CANCELED"
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor"
}
"""

class UpdateOvertimeRequestStatus:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    overtime = inject.attr(Overtime)
    date = inject.attr(Date)
    events = inject.attr(Events)

    def handleAction(self, server, message):

        if (message['action'] != 'updateOvertimeRequestStatus'):
            return False

        if ('session' not in message) or ('request' not in message) or ('request_id' not in message['request']) or ('status' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        requestId = message['request']['request_id']
        status = message['request']['status']

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])
        userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            events = self.overtime.updateOvertimeRequestStatus(con,userId,requestId,status)
            con.commit()

            response = {
                'id':message['id'],
                'ok':'El cambio se ha realizado correctamente'
            }
            server.sendMessage(response)

            for e in events:
                self.events.broadcast(server,e)

            return True

        except Exception as e:
            logging.exception(e)
            con.rollback()

            response = {
                'id':message['id'],
                'error':'Error realizando pedido'
            }
            server.sendMessage(response)
            return True

        finally:
            con.close()




"""
query : solicitud de justificaciones de un determinado usuario
{
  id:,
  action:"requestOvertime",
  session:,
  request:{
      user_id: "id del usuario al cual se le solicita el tiempo extra",
  	  begin: "timestamp de inicio del tiempo extra"
  	  end: "timestamp de fin del tiempo extra"
  	  reason: "motivo de solicitud del tiempo extra"
  }
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor"
}
"""

class RequestOvertime:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    overtime = inject.attr(Overtime)
    date = inject.attr(Date)
    events = inject.attr(Events)

    def handleAction(self, server, message):

        if (message['action'] != 'requestOvertime'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']) or ('justification_id' not in message['request']) or ('begin' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True


        userId = message['request']['user_id']
        begin = message['request']['begin']
        begin = self.date.parse(begin)
        end = None
        if 'end' in message['request']:
            end = message['request']['end']
            end = self.date.parse(end)


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        requestorId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            events = self.overtime.requestOvertime(con,requestorId,userId,begin,end)

            con.commit()

            response = {
                'id':message['id'],
                'ok':'El pedido se ha realizado correctamente'
            }
            server.sendMessage(response)

            for e in events:
                self.events.broadcast(server,e)

            return True


        except Exception as e:
            logging.exception(e)
            con.rollback()

            response = {
                'id':message['id'],
                'error':'Error realizando pedido'
            }
            server.sendMessage(response)
            return True

        finally:
            con.close()
