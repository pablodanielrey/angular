# -*- coding: utf-8 -*-
import psycopg2
import json, uuid, inject
from model.systems import Systems
from model.profiles import Profiles
from model.config import Config
from model.events import Events
from model.objectView import ObjectView

"""
peticion:
{
    "id":"",
    "action":"listSystems"
    "session":"sesion de usuario"
}

respuesta:
{
    "id":"id de la petición",
    "systems":[
        {
         "id":"",
         "name":"",
         "config":"",
        }
      ],
    "ok":"",
    "error":""
}

"""

class ListSystems:

  systems = inject.attr(Systems)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if message['action'] != 'listSystems':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      rdata = self.systems.listSystems(con)

      response = {'id':message['id'], 'ok':'', 'systems': rdata}
      server.sendMessage(response)
      return True

    finally:
        con.close()
