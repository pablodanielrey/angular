# -*- coding: utf-8 -*-
import json, uuid, psycopg2, re
import inject
import hashlib

from model.users.users import Users
from model.events import Events
from model.profiles import Profiles
from model.config import Config

from wexceptions import *


"""
peticion:
{
    "id":"",
    "action":"updateUser"
    "session":"sesion de usuario"
    "user":{
        "id":"id de usuario",
        "name":'nombre',
        "lastname":'apellido',
        "dni":"dni",
        'city':"ciudad actual"
        'country':"pais actual"
        'address':"direccion actual"
        'genre':"género"
        'birthdate':"fecha de nacimiento"
        'telephones':[{
        	'number':"numero"
        	'type':"tipo"
        }]
    }
}

respuesta:
{
    "id":"id de la petición",
    "ok":"",
    "error":""
}

"""

class UpdateUser:

  req = inject.attr(Users)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)


  def handleAction(self, server, message):

    if (message['action'] != 'updateUser'):
        return False


    if 'user' not in message:
        raise MalformedMessage()

    if 'id' not in message['user']:
        raise MalformedMessage()

    if message['user']['id'] == None:
        raise MalformedMessage()


    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      user = message['user']
      if user == None:
          raise MalformedMessage()

      self.req.updateUser(con,user);
      con.commit()

      response = {'id':message['id'], 'ok':''}
      server.sendMessage(response)

      event = {
        'type':'UserUpdatedEvent',
        'data':user['id']
      }
      self.events.broadcast(server,event)
      return True

    except psycopg2.DatabaseError as e:
        con.rollback()
        raise e

    finally:
        con.close()





"""

peticion:
{
    "id":"",
    "action":"findUser"
    "session":"sesion de usuario"
    "user":{
        "id":"id de usuario"
    }
}

respuesta:
{
    "id":"id de la petición",
    "user":[
        {
        "id":"id de usuario",
        "name":'nombre',
        "lastname":'apellido',
        "dni":"dni",
        'city':"ciudad actual"
        'country':"pais actual"
        'address':"direccion actual"
        'genre':"género"
        'birthdate':"fecha de nacimiento"
        }
      ],
    "ok":"",
    "error":""
}

"""

class FindUser:

  req = inject.attr(Users)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)


  def handleAction(self, server, message):

    if (message['action'] != 'findUser'):
        return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      if ((message['user'] == None) or (message['user']['id'] == None)):
          raise MalformedMessage()

      id = message['user']['id']
      user = self.req.findUser(con,id)
      response = {'id':message['id'], 'ok':'', 'user': user}
      server.sendMessage(response)
      return True

    finally:
        con.close()





"""
peticion:
{
    "id":"",
    "action":"listUsers"
    "session":"sesion de usuario"
-   "onlyIds":"True|False"
-   "ids":"[ids de los usuarios a retornar en el listado]"
}

respuesta:
{
    "id":"id de la petición",
    "users":[
        {
         "id":"",
         "dni":"",
         "name":"",
         "lastname":""
        }
      ],
    "ok":"",
    "error":""
}

"""

class ListUsers:

  req = inject.attr(Users)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if message['action'] != 'listUsers':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      rdata = self.req.listUsers(con)

      if 'search' in message:
        rdataAux = []
        pattern = re.compile(message['search'],re.IGNORECASE)
        for user in rdata:
      	  if pattern.search(user["name"]) or pattern.search(user["name"] + " " + user["lastname"]) or pattern.search(user["lastname"] + " " + user["name"]) or pattern.search(user["lastname"]) or pattern.search(user["dni"]):
            rdataAux.append(user)
        rdata = rdataAux

      if 'limit' in message:
        del rdata[message['limit']:]

      if 'onlyIds' in message:
          rdata = [{'id':x['id']} for x in rdata]

      if 'ids' in message:
          rdata = [x for x in rdata if x['id'] in message['ids']]



      response = {'id':message['id'], 'ok':'', 'users': rdata}
      server.sendMessage(response)
      return True

    finally:
        con.close()
