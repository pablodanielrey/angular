# -*- coding: utf-8 -*-
import inject
import json
import uuid
import re
import logging
import psycopg2
import hashlib
import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
from model.config import Config

from model.users.users import Users
from model.events import Events
from model.profiles import Profiles
from model.config import Config

from model.exceptions import *


class UsersWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.findById_async, 'users.findById')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def findById(self, id):
        con = self._getDatabase()
        try:
            # codigo
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def findById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findById, id)
        return r


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