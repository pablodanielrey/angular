# -*- coding: utf-8 -*-.
import json, base64, traceback, logging
import inject, psycopg2
import pytz, datetime
import dateutil.parser

from model.exceptions import *

from model.config import Config
from model.profiles import Profiles
from model.utils import DateTimeEncoder
from model.events import Events

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
    events = inject.attr(Events)
    
    
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
        state = 'PENDING' if (('state' not in message['request']) or (message['request']['state'] is None)) else message['request']['state']
        relatedRequestId = None if (('relatedRequestId' not in message['request']) or (message['request']['relatedRequestId'] is None)) else message['request']['relatedRequestId']
        
        #definir conexion con la base de datos
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
      
        try:
        
            #abcm datos
            events = self.issue.insert(con, request, officeId, requestorId, created, priority, visibility, relatedRequestId, state)
            con.commit()
            
            #disparar eventos
            for e in events: 
                self.events.broadcast(server,e) 

            
        except Exception as e:
            logging.exception(e)
            raise e;

        finally:
            con.close()


       
""" 
peticion: 
{ 
	  "id":"", 
	  "action":"getIssuesByUser", 
	  "session":"session de usuario", 
	  "request":{ 
       userId: Id de usuario
    } 
} 

respuesta: 
{ 
	  "id":"id de la peticion", 
	  "ok":"", 
	  "error":"" 
} 

"""
class GetIssuesByUser:
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    
    issue = inject.attr(Issue)
        
      
    def handleAction(self, server, message):
        if (message['action'] != 'getIssuesByUser'): 
            return False
            
        #chequear parametros
        if ('id' not in message) or ('session' not in message) or ('request' not in message) or ('userId' not in message['request']): 
            response = {'id':message['id'], 'error':'Insuficientes parámetros'} 
            server.sendMessage(response) 
            return True 
           
        #chequear permisos
        sid = message['session'] 
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])
        
        #definir datos
        userId = message['request']['userId']
    
        #definir conexion con la base de datos
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        
        
        try: 
            data = self.issue.getIssuesByUser(con,userId)
            
             #enviar mensaje de respuesta
            response = { 
                'id':message['id'], 
                'ok':'',
                'response':data
            } 
            server.sendMessage(response)
        except Exception as e: 
            logging.exception(e) 
            
            con.rollback() 

            response = { 
             'id':message['id'], 
             'error':'Error realizando pedido' 
            } 
            server.sendMessage(response) 
            
        finally: 
            con.close()
            return True 
            
            
""" 
peticion: 
{ 
	  "id":"", 
	  "action":"deleteIssue", 
	  "session":"session de usuario", 
	  "request":{ 
        id Id del nodo a eliminar
     } 
} 

respuesta: 
{ 
	  "id":"id de la peticion", 
	  "ok":"", 
	  "error":"" 
} 

"""            
class DeleteIssue: 

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    events = inject.attr(Events)
    
    issue = inject.attr(Issue)
    
    
    """ manejar accion """
    def handleAction(self, server, message): 

        if (message['action'] != 'deleteIssue'): 
            return False

        #chequear parametros
        if ('id' not in message) or ('session' not in message) or ('request' not in message) or ('id' not in message['request']): 
           response = {'id':message['id'], 'error':'Insuficientes parámetros'} 
           server.sendMessage(response) 
           return True 
    
        #chequear permisos
        sid = message['session'] 
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        #definir datos
        id = message['request']['id']

        #definir conexion con la base de datos
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try: 

            #abcm datos
            events = self.issue.deleteIssue(con,id) 
            con.commit()

            """ enviar mensaje de respuesta """
            response = { 
              'id':message['id'], 
              'ok':'La eliminacion se ha realizado correctamente' 
            } 
            server.sendMessage(response) 

            """ disparar eventos """
            for e in events: 
              self.events.broadcast(server,e) 

        except Exception as e: 
            logging.exception(e) 
            con.rollback() 

            response = { 
              'id':message['id'], 
              'error':'Error realizando pedido' 
            } 
            server.sendMessage(response) 

        finally: 
            con.close()
            return True



"""
query :
{
  id:,
  action:"updateIssueData",
  session:,
  issue:{  "Datos del pedido"

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
class UpdateIssueData: 

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    date = inject.attr(Date)
    events = inject.attr(Events)
    
    issue = inject.attr(Issue)


    """ manejar accion """
    def handleAction(self, server, message): 

        if (message['action'] != 'updateIssueData'): 
            return False


        #chequear parametros
        if ('id' not in message) or ('session' not in message) or ('issue' not in message) or ('id' not in message['issue']) or ('request' not in message['issue']) or ('state' not in message['issue']) or ('userId' not in message):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'} 
            server.sendMessage(response) 
            return True 

    
        #chequear permisos
        sid = message['session'] 
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])


        #definir datos
        id = message['issue']['id']
        request = message['issue']['request']
        state = message['issue']['state']
        priority = 0 if (('priority' not in message['issue']) or (message['issue']['priority'] is None)) else message['issue']['priority']
        visibility = 'AUTHENTICATED' if (('visibility' not in message['issue']) or (message['issue']['visibility'] is None)) else message['issue']['visibility']
        userId = message["userId"]
        
        #definir conexion con la base de datos
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
      
        try:
        
            #abcm datos
            events = self.issue.updateData(con, id, request, priority, visibility, state, userId)
            con.commit()
            
            #disparar eventos
            for e in events: 
                self.events.broadcast(server,e) 

            
        except Exception as e:
            logging.exception(e)
            raise e;

        finally:
            con.close()
