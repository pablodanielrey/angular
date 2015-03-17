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
            
