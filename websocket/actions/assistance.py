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

    def handleAction(self, server, message):

        if (message['action'] != 'getAssistanceStatus'):
            return False

        if 'domain' not in message:
            response = {"id":message['id'], 'error':'no existe la info correspondiente al dominio'}
            server.sendMessage(response)
            return True

        if 'id' not in message['domain']:
            response = {"id":message['id'],'error':'el usuario no posee id'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            domain = message['domain']
            self.req.persistDomain(con,domain)
            con.commit()

            response = {'id':message['id'], 'ok':''}
            server.sendMessage(response)

            event = {
                'type':'UserDomainUpdatedEvent',
                'data':domain['id']
            }
            self.events.broadcast(server,event)

            return True
        except psycopg2.DatabaseError, e:
            con.rollback()
            raise e

        finally:
            con.close()
