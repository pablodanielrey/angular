# -*- coding: utf-8 -*-
import psycopg2
import json, uuid, inject
from model.groups import Groups
from model.profiles import Profiles
from model.config import Config
from model.events import Events
from model.objectView import ObjectView


"""

peticion:
{
    "id":"",
    "action":"createGroup"
    "session":"sesion de usuario"
    "group":{
        "systemId":'id de sistema',
        "name":'nombre del grupo'
    }
}

respuesta:
{
    "id":"id de la petición",
    "ok":"",
    "error":""
}

"""

class CreateGroup:

  groups = inject.attr(Groups)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)
  events = inject.attr(Events)


  def handleAction(self, server, message):

    if (message['action'] != 'createGroup'):
        return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      if ((message['group'] == None) or (message['group']['systemId'] == None) or (message['group']['name'] == None)):
          raise MalformedMessage()


      id = str(uuid.uuid4())
      message['group']['id'] = id
      group = ObjectView(message['group'])
      self.groups.createGroup(con,group)
      con.commit()

      response = {'id':message['id'], 'ok':'' }
      server.sendMessage(response)


      event = {
        'type':'GroupCreatedEvent',
        'data':group.id
      }
      self.events.broadcast(server,event)

      return True

    finally:
        con.close()


"""

peticion:
{
    "id":"",
    "action":"updateGroup"
    "session":"sesion de usuario"
    "group":{
        "id":"id de grupo",
        "systemId":'id de sistema',
        "name":'nombre del grupo'
    }
}

respuesta:
{
    "id":"id de la petición",
    "ok":"",
    "error":""
}

"""

class UpdateGroup:

  groups = inject.attr(Groups)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)
  events = inject.attr(Events)


  def handleAction(self, server, message):

    if (message['action'] != 'updateGroup'):
        return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      if ((message['group'] == None) or (message['group']['id'] == None)):
          raise MalformedMessage()

      group = ObjectView(message['group'])
      self.groups.updateGroup(con,group)
      con.commit()

      response = {'id':message['id'], 'ok':'' }
      server.sendMessage(response)


      event = {
        'type':'GroupUpdatedEvent',
        'data':group.id
      }
      self.events.broadcast(server,event)

      return True

    finally:
        con.close()



"""

peticion:
{
    "id":"",
    "action":"addMembers"
    "session":"sesion de usuario"
    "group":{
        "id":"id de grupo",
        "members": [
            {
                id: "id de usuario a agregar"
            }
        ]
    }
}

respuesta:
{
    "id":"id de la petición",
    "ok":"",
    "error":""
}

"""

class AddMembers:

  groups = inject.attr(Groups)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)
  events = inject.attr(Events)


  def handleAction(self, server, message):

    if (message['action'] != 'addMembers'):
        return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      if ((message['group'] == None) or (message['group']['id'] == None)):
          raise MalformedMessage()

      id = message['group']['id']
      members = message['group']['members']
      self.groups.addMembers(con,id,members)
      con.commit()

      response = {'id':message['id'], 'ok':'' }
      server.sendMessage(response)


      event = {
        'type':'GroupUpdatedEvent',
        'data':id
      }
      self.events.broadcast(server,event)

      return True

    finally:
        con.close()




"""

peticion:
{
    "id":"",
    "action":"removeMembers"
    "session":"sesion de usuario"
    "group":{
        "id":"id de grupo",
        "members": [
            {
                id: "id de usuario a remover"
            }
        ]
    }
}

respuesta:
{
    "id":"id de la petición",
    "ok":"",
    "error":""
}

"""

class RemoveMembers:

  groups = inject.attr(Groups)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)
  events = inject.attr(Events)


  def handleAction(self, server, message):

    if (message['action'] != 'removeMembers'):
        return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      if ((message['group'] == None) or (message['group']['id'] == None)):
          raise MalformedMessage()

      id = message['group']['id']
      members = message['group']['members']
      self.groups.removeMembers(con,id,members)
      con.commit()

      response = {'id':message['id'], 'ok':'' }
      server.sendMessage(response)


      event = {
        'type':'GroupUpdatedEvent',
        'data':id
      }
      self.events.broadcast(server,event)

      return True

    finally:
        con.close()



"""

peticion:
{
    "id":"",
    "action":"findMembers"
    "session":"sesion de usuario"
    "group":{
        "id":"id de grupo"
    }
}

respuesta:
{
    "id":"id de la petición",
    "group":[
        {
        "id":"id del grupo",
        "members": [
                {
                    id: 'id de usuario'
                }
            ]
        }
      ],
    "ok":"",
    "error":""
}

"""

class FindMembers:

  groups = inject.attr(Groups)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)


  def handleAction(self, server, message):

    if (message['action'] != 'findMembers'):
        return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      if ((message['group'] == None) or (message['group']['id'] == None)):
          raise MalformedMessage()

      id = message['group']['id']
      members = self.groups.findMembers(con,id)
      group = {
        'id':id,
        'members':members
      }
      response = {'id':message['id'], 'ok':'', 'group':group }
      server.sendMessage(response)
      return True

    finally:
        con.close()


"""

peticion:
{
    "id":"",
    "action":"findGroup"
    "session":"sesion de usuario"
    "group":{
        "id":"id de grupo"
    }
}

respuesta:
{
    "id":"id de la petición",
    "group":[
        {
        "id":"id",
        "name":'nombre',
        "system_id":'id del sistema',
        }
      ],
    "ok":"",
    "error":""
}

"""

class FindGroup:

  groups = inject.attr(Groups)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)


  def handleAction(self, server, message):

    if (message['action'] != 'findGroup'):
        return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      if ((message['group'] == None) or (message['group']['id'] == None)):
          raise MalformedMessage()

      id = message['group']['id']
      group = self.groups.findGroup(con,id)
      response = {'id':message['id'], 'ok':'', 'group': group}
      server.sendMessage(response)
      return True

    finally:
        con.close()



"""
peticion:
{
    "id":"",
    "action":"listGroups"
    "session":"sesion de usuario"
}

respuesta:
{
    "id":"id de la petición",
    "groups":[
        {
         "id":"",
         "system_id":"",
         "name":"",
        }
      ],
    "ok":"",
    "error":""
}

"""

class ListGroups:

  groups = inject.attr(Groups)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if message['action'] != 'listGroups':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      rdata = self.groups.listGroups(con)

      response = {'id':message['id'], 'ok':'', 'groups': rdata}
      server.sendMessage(response)
      return True

    finally:
        con.close()
