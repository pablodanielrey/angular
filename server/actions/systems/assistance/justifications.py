# -*- coding: utf-8 -*-
import json, base64, datetime, traceback, logging
import inject
import psycopg2

from wexceptions import *

from model.config import Config
from model.profiles import Profiles

from model.systems.assistance.assistance import Assistance
from model.systems.assistance.date import Date
from model.systems.assistance.justifications import Justifications



"""

query :
{
  id:,
  action:"getJustifications",
  session:
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    justifications: [
      {
        id: 'id de la justificacion',
        name: 'nombre de la justificacion'
      }
    ]
  }

}
"""


class GetJustifications:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)

    def handleAction(self, server, message):

        if (message['action'] != 'getJustifications'):
            return False

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            justs = self.justifications.getJustifications(con)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'justifications':justs
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            con.rollback()
            raise e

        finally:
            con.close()







"""
query :
{
  id:,
  action:"getJustificationStock",
  session:,
  request:{
      user_id: "id del usuario",
      justification_id: "id de la justificación"
      date: 'fecha a consultar'                         -- opcional. si no se pasa etnonces se toma la fecha actual.
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    count: "cantidad de justificaciones disponibles de ese tipo"
  }

}

"""

class GetJustificationStock:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)
    date = inject.attr(Date)

    def handleAction(self, server, message):

        if (message['action'] != 'getJustificationStock'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']) or ('justification_id' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        userId = message['request']['user_id']
        justificationId = message['request']['justification_id']

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            date = self.date.utcNow()

            stock = self.justifications.getJustificationStock(con,userId,justificationId,date)
            if stock == None:
                response = {'id':message['id'], 'error':'No existe stock para esa justificación'}
                server.sendMessage(response)
                return True

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'justificationId':justificationId,
                    'stock':stock
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()





"""
query : Obtener todas las solicitudes de justificationces
{
  id:,
  action:"getJustificationRequests",
  session:,
  request:{
      status: 'estado de la justificacion PENDING|APPROVED|REJECTED|CANCELED' -- si no existe se obtienen todas,
      group: "ROOT|TREE" -- si no existe obtiene solo las del usuario, y no las del grupo
  }
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    requests : [ "lista de solicitudes de un determinado usuario"
  		{
        id: "id de la solicitud de justificacion",
        user_id:"id del usuario",
    		justification_id: "id de la justificacion o licencia solicitada"
    		begin: 2014-12-01 00:00:00 "fecha de inicio de la justificacion o licencia solicitada"
    		end: 2014-12-02 00:00:00 "fecha de finalizacion de la justificacion o licencia solicitada"
    		status: "PENDING|APPROVED|REJECTED|CANCELED"
  		}
	]

}
"""

class GetJustificationRequests:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    assistance = inject.attr(Assistance)

    def handleAction(self, server, message):

        if (message['action'] != 'getJustificationRequests'):
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
            requests = self.assistance.getJustificationRequests(con,userId,status,group)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'requests':requests
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()





"""
query : solicitud de justificaciones de un determinado usuario
{
  id:,
  action:"requestJustification",
  session:,
  request:{
      user_id: "id del usuario",
      justification_id: "id de la justificacion o licencia solicitada"
  	  begin: "fecha de inicio de la justificacion o licencia solicitada"
  	  end: "fecha de finalizacion de la justificacion o licencia solicitada" -- algunas justificaciones no tienen fin. es el turno completo.
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor"
}
"""

class RequestJustification:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)
    date = inject.attr(Date)

    def handleAction(self, server, message):

        if (message['action'] != 'requestJustification'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']) or ('justification_id' not in message['request']) or ('begin' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True


        userId = message['request']['user_id']
        justificationId = message['request']['justification_id']
        begin = message['request']['begin']
        begin = self.date.parse(begin)
        end = None
        if 'end' in message['request']:
            end = message['request']['end']
            end = self.date.parse(end)


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            self.justifications.requestJustification(con,userId,justificationId,begin,end)

            con.commit()

            response = {
                'id':message['id'],
                'ok':'El pedido se ha realizado correctamente'
            }
            server.sendMessage(response)
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
