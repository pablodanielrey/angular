# -*- coding: utf-8 -*-
import json, base64, datetime, traceback, logging, inject, psycopg2

from wexceptions import *

from model.config import Config
from model.profiles import AccessDenied, Profiles
from model.utils import DateTimeEncoder

from model.systems.assistance.logs import Logs


"""
query :
{
  id:,
  action:'getAssistanceLogs',
  session:,
  request:{
    user_id:'id del usuario'
    from: 'fecha en ISO 8601 con info utc, YYYY-MM-DDTHH:MM:SS+HH:MM' -- opcional,
    to: 'fecha en ISO 8601 con info utc, YYYY-MM-DDTHH:MM:SS+HH:MM' -- opcional
  }
}

{"id":"2","action":"getAssistanceLogs","session":"sfdsfds","request":{"user_id":"7872c56b-881a-4025-9526-5a537789ce5c"}}

response:
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    logs: [
      {
        id:'id del log',
        log: 'fecha en ISO 8601 con info utc, YYYY-MM-DDTHH:MM:SS+HH:MM',
        verifymode: n,
        deviceId: 'id del dispositivo',
        userId: 'id del usuario'
      }
    ]
  }
}

"""

class GetAssistanceLogs:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    logs = inject.attr(Logs)

    def handleAction(self, server, message):

        if (message['action'] != 'getAssistanceLogs'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN'])
        """


        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            userId = message['request']['user_id']

            logging.debug('obteniendo logs para el usuario ' + userId)

            logs = self.logs.findLogs(con,userId)

            logging.debug('logs obtenidos para el usuario')

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'logs':logs
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            con.rollback()
            raise e

        finally:
            con.close()
