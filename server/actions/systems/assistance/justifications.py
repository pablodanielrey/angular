# -*- coding: utf-8 -*-
import json, base64, datetime, traceback, logging
import inject
import psycopg2

from wexceptions import *

from model.config import Config
from model.profiles import Profiles

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
query : Obtener solicitudes de justificationces de un determinado usuario
{
  id:,
  action:"getJustificationRequests",
  session:,
  request:{
      user_id: "id del usuario",
      status: 'estado de la justificacion PENDING|APPROVED|REJECTED|CANCELED' -- si no existe se obtienen todas
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
    		justification_id: "id de la justificacion o licencia solicitada"
    		begin: 2014-12-01 00:00:00 "fecha de inicio de la justificacion o licencia solicitada"
    		end: 2014-12-02 00:00:00 "fecha de finalizacion de la justificacion o licencia solicitada"
    		state: "PENDING|APPROVED|REJECTED|CANCELED"
  		}
	]

}
"""
class GetJustificationRequests:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if (message['action'] != 'getJustificationRequests'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        userId = message['request']['user_id']
        status = None
        if 'status' in message['request']:
            status = message['request']


        """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])
        """

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            requests = assistance.getJustificationRequests(con,userId,status)

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
            con.rollback()
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
  	  end: "fecha de finalizacion de la justificacion o licencia solicitada" -- si no viene en el mensaje se toma hasta el fin de turno
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor"
}
"""

class requestJustification:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if (message['action'] != 'requestJustification'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']) or ('justification_id' not in message['request']) or ('begin' not in message['requesst']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        userId = message['request']['user_id']

        req = {
            'justificationId':message['request']['justification_id'],
            'begin':message['request']['begin']
        }
        if 'end' in message['request']:
            req['end'] = message['request']['end']


        """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])
        """

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            assistance.requestJustification(con,userId,req)

            response = {
                'id':message['id'],
                'ok':'El pedido se ha realizado correctamente'
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            con.rollback()

            response = {
                'id':message['id'],
                'error':'Error realizando pedido'
            }
            server.sendMessage(response)
            return True

        finally:
            con.close()
