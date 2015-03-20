# -*- coding: utf-8 -*-
from Ws.SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import json, base64
import datetime
import traceback
import logging
from wexceptions import MalformedMessage
from model.profiles import AccessDenied
from model.utils import DateTimeEncoder







"""
query :
{
  id:,
  action:"getAssistanceStatus",
  session:,
  request:{
      user_id: "id del usuario"
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
      status: 'estado del agente ',
      start: "fecha y hora de inicio para el dia actual",
      end: "fecha y hora fin para el dia actual",
      logs: [ date1, date2, date3, .... ]       // son todas las marcaciones en bruto del dia actual
      workedMinutes: 'minutos trabajados dentro del dia actual'
  }

}
"""


class GetAssistanceStatus:

    req = inject.attr(Domain)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    assitance = inject.attr(Assistance)

    def handleAction(self, server, message):

        if (message['action'] != 'getAssistanceStatus'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            status = assistance.getAssistanceStatus(con,message['request']['user_id'])

            response = {
                'id':message['id'],
                'ok':'',
                'response':status
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError, e:
            con.rollback()
            raise e

        finally:
            con.close()


"""

{
  id:,
  action:"getAssistanceData",
  session:,
  request:{
    user_id: "id del usuario",
    date: "fecha a consultar" -- en caso de que no exista consulta el día actual.
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
      position: 'cargo de la persona',
  	  schedule:[
    		{
    	       start: "fecha y hora de inicio del turno",
    		   end: "fecha y hora de fin de turno"
    		}
  	  ]
  }

}

"""

class GetAssistanceData:

    req = inject.attr(Domain)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    assitance = inject.attr(Assistance)

    def handleAction(self, server, message):

        if (message['action'] != 'getAssistanceData'):
            return False

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True


        """ precondiciones del request """
        request = message['request']

        if 'user_id' not in request:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        userId = request['user_id']

        date = datetime.date.now()
        if 'date' in request:
            date = time.strptime(request['date'])

        """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])
        """

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            status = assistance.getAssistanceData(con,userId,date)

            response = {
                'id':message['id'],
                'ok':'',
                'response':status
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError, e:
            con.rollback()
            raise e

        finally:
            con.close()



"""

query :
{
  id:,
  action:"getOffices",
  session:,
  request:{
      user_id: "id del usuario" -- opcional. si no existe el parámetro entonces retorna todas las oficinas.
      tree: "True|False" -- obtiene todo el arbol de las oficinas abajo de las que la persona pertenece.
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    offices: [
      {
        id: 'id de la oficina',
        name: 'nombre de la oficina',
        parent: 'id de la oficina padre' -- o no existente en el caso de ser oficina de primer nivel.
      }
    ]
  }

}


"""

class GetOffices:

    req = inject.attr(Domain)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    assitance = inject.attr(Assistance)

    def handleAction(self, server, message):

        if (message['action'] != 'getOffices'):
            return False

        userId = None
        if 'request' in message and 'user_id' in message['request']:
            userId = message['request']['user_id']


        tree = False
        if 'request' in message and 'tree' in message['request']:
            tree = message['request']['tree']


        """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])
        """

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            offices = []
            if userId == None:
                offices = assistance.getOfficesByUser(con,userId,tree)
            else:
                offices = assistance.getOffices(con)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'offices':offices
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError, e:
            con.rollback()
            raise e

        finally:
            con.close()

            
