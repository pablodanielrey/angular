# -*- coding: utf-8 -*-.
import json, base64, traceback, logging
import inject, psycopg2
import pytz, datetime
import dateutil.parser

from model.exceptions import *

from model.config import Config
from model.profiles import Profiles
from model.utils import DateTimeEncoder

from model.systems.assistance.date import Date
from model.systems.issue.issue import Issue




"""
query :
{
  id:,
  action:"newRequest",
  session:,
  request:{
     request:"Descripcion del pedido"
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{[
      user: 'datos del usuario ',
      fail: "datos correspondiente a la falla"
  ]}

}
"""

class NewRequest:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    date = inject.attr(Date)
    
    issue = inject.attr(Issue)

    def handleAction(self, server, message):

        if (message['action'] != 'newIssueRequest'): 
            return False

        #chequear parametros
        if ('id' not in message) or ('session' not in message) or ('request' not in message) or ('request' not in message['request']) or ('requestorId' not in message['request']) or ('officeId' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'} 
            server.sendMessage(response) 
            return True 
        
        #chequear permisos
        sid = message['session'] 
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])
        
        #definir datos
        officeId = message['request']['officeId']
        requestorId = message['request']['requestorId']
        request = message['request']['request']
        created = self.utcNow() if (('created' not in message['request']) or (message['request']['created'] is None)) else self.date.parse(message['request']['created'])
        priority = 0 if (('priority' not in message['request']) or (message['request']['priority'] is None)) else message['request']['priority']
        visibility = 'AUTHENTICATED' if (('visibility' not in message['request']) or (message['request']['visibility'] is None)) else message['request']['visibility']
        relatedRequestId = None if (('relatedRequestId' not in message['request']) or (message['request']['relatedRequestId'] is None)) else message['request']['relatedRequestId']
        
        #definir conexion con la base de datos
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
      
        try:
        
            #abcm datos
            events = self.issue.insert(con, request, officeId, requestorId, created, priority, visibility, relatedRequestId)
            con.commit()
            
        except Exception as e:
            logging.exception(e)
            raise e;

        finally:
            con.close()
        
      
       


