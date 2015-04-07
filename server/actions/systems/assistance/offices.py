# -*- coding: utf-8 -*-
import json, base64, datetime, traceback, logging
import inject
import psycopg2

from wexceptions import *

from model.config import Config
from model.profiles import Profiles

from model.utils import DateTimeEncoder

from model.systems.assistance.offices import Offices



"""
retorna los usuarios que pertenecen a las oficinas y suboficinas en las cuales la persona userId tiene un rol determinado

query:
{
  id:
  action:'getUserInOfficesByRole'
  session:
  request: {
    userId: id del usuario que tiene los roles en las oficinas -- opcional,. si no va se toma el usuario actual de la session
    role: rol a buscar
    tree: False|True -- retorna el arbol o solo las oficinas directas que tienen el rol.
  }
}

response:
{
  id:
  ok:
  error:
  response: {
    users: [
        userId: 'id del usuario'
    ]
  }
}

"""
class GetUserInOfficesByRole:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'getUserInOfficesByRole'):
            return False

        if 'role' not in message['request']:
            raise MalformedMessage()

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        userId = self.profiles.getLocalUserId(sid)
        if 'userId' in message['request']:
            userId = message['request']['userId']

        tree = False
        if 'tree' in message['request']:
            tree = message['request']['tree']

        role = message['request']['role']

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            logging.debug('getUserInOfficesByRole')
            users = self.offices.getUserInOfficesByRole(con,userId,tree,role)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'users':users
                }
            }
            server.sendMessage(response)
            return True

        except Exception as e:
            logging.exception(e)
            raise e

        finally:
            con.close()




"""
query:
{
  id:
  action:'getUserOfficeRoles'
  session:
  request: {
    officeId: 'id de la oficina' -- opcional, en el caso de no existir obtiene todos los roles que tenga en las oficinas
  }
}

response:
{
  id:
  ok:
  error:
  response: {
    roles: [
      {
        officeId: 'id de la oficina',
        role: 'rol en la oficina'
      }
    ]
  }
}

"""
class GetUserOfficeRoles:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'getUserOfficeRoles'):
            return False

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])
        userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            roles = self.offices.getOfficesRoles(con,userId)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'roles':roles
                }
            }
            server.sendMessage(response)
            return True

        except Exception as e:
            logging.exception(e)
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

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'getOffices'):
            return False

        userId = None
        if 'request' in message and 'user_id' in message['request']:
            userId = message['request']['user_id']


        tree = False
        if 'request' in message and 'tree' in message['request']:
            tree = message['request']['tree']


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            offices = []
            if userId is not None:
                offices = self.offices.getOfficesByUser(con,userId,tree)
            else:
                offices = self.offices.getOffices(con)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'offices':offices
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()
