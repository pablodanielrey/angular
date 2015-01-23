# -*- coding: utf-8 -*-
import json, uuid, psycopg2, inject
import hashlib
from model.requests import Requests
from model.users import Users
from model.objectView import ObjectView
from model.events import Events
from model.profiles import Profiles
from model.mail import Mail
from model.config import Config
from model.userPassword import UserPassword
from wexceptions import MalformedMessage


"""
    Modulo de acceso a la capa de las peticiones de cuentas.

"""


"""
peticion:
{
  "id":"id de la peticion"
  "action":"removeAccountRequest",
  "session":"id de session obtenido en el login",
  "reqId":"id del request a eliminar"
}

respuesta:
{
  "id":"id de la peticion"
  O "ok":""
  O "error":""
}

"""


class RemoveAccountRequest:

  req = inject.attr(Requests)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if message['action'] != 'removeAccountRequest':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])

    if 'id' not in message:
        raise MalformedMessage()

    if 'reqId' not in message:
        raise MalformedMessage()

    pid = message['id']
    rid = message['reqId']

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      self.req.removeRequest(con,rid)
      con.commit()

      response = {'id':pid, 'ok':'petición eliminada correctamente'}
      server.sendMessage(response)

      event = {
        'type':'AccountRequestRemovedEvent',
        'data': rid
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
  "id":"id de la peticion"
  "action":"createAccountRequest"

  "request":{
    "dni":""
    "name":""
    "lastname":""
    "email":""
    "reason":""
  }
}

respuesta:
{
  "id":"id de la peticion"
  O "ok":""
  O "error":""
}

"""


class CreateAccountRequest:

  req = inject.attr(Requests)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if message['action'] != 'createAccountRequest':
      return False

    if 'id' not in message:
        raise MalformedMessage()

    if 'request' not in message:
        raise MalformedMessage()

    pid = message['id']

    data = message['request']
    data['id'] = str(uuid.uuid4());

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      self.req.createRequest(con,data)
      con.commit()

      response = {'id':pid, 'ok':'petición creada correctamente'}
      server.sendMessage(response)

      event = {
        'type':'NewAccountRequestEvent',
        'data': data['id']
      }
      self.events.broadcast(server,event)

      return True

    finally:
        con.close()






"""
peticion:
{
    "id":"",
    "action":"listAccountRequests"
    "session":"sesion de usuario"
}

respuesta:
{
    "id":"id de la petición",
    "requests":[
        {
         "id":"",
         "dni":"",
         "name":"",
         "lastname":"",
         "email":""
        }
      ],
    "ok":"",
    "error":""
}

"""

class ListAccountRequests:

  req = inject.attr(Requests)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if message['action'] != 'listAccountRequests':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      rdata = self.req.listRequests(con)
      response = {'id':message['id'], 'ok':'', 'requests': rdata}
      server.sendMessage(response)
      return True

    finally:
        con.close()






"""
peticion:
{
  "id":"id de la peticion"
  "action":"aprobeAccountRequest",
  "session":"id de session obtenido en el login",
  "reqId":"id de la peticion"
}

respuesta:
{
  "id":"id de la peticion"
  O "ok":""
  O "error":""
}

eventos :

AccountRequestAprovedEvent
UserUpdatedEvent

"""

class ApproveAccountRequest:

  req = inject.attr(Requests)
  users = inject.attr(Users)
  profiles = inject.attr(Profiles)
  events = inject.attr(Events)
  mail = inject.attr(Mail)
  userPass = inject.attr(UserPassword)
  config = inject.attr(Config)


  def sendEvents(self,server,req_id,user_id):
      event = {
        'type':'AccountRequestApprovedEvent',
        'data':req_id
      }
      self.events.broadcast(server,event)

      event = {
        'type':'UserUpdatedEvent',
        'data':user_id
      }
      self.events.broadcast(server,event)


  def sendNotificationMail(self,request):
      pass


  def handleAction(self, server, message):

    if message['action'] != 'approveAccountRequest':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])

    pid = message['id']
    reqId = message['reqId']

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      req = self.req.findRequest(con,reqId)
      if (req == None):
          raise MalformedMessage()

      user = self.users.findUserByDni(con,req['dni'])
      if user != None:
          raise DupplicatedUser()

      user = {
        'dni':req['dni'],
        'name':req['name'],
        'lastname':req['lastname']
      }
      user_id = self.users.createUser(con,user)
      self.users.createMail(con,{
            'user_id':user_id,
            'email':req['email']
      })

      """
      ''' autogenero un password usando sha1 y uuid '''
      creds = {
        'user_id':user_id,
        'username':user['dni'],
        'password': hashlib.sha1(str(uuid.uuid4())).hexdigest()
      }
      """
      ''' uso la clave que pidio en el request '''
      creds = {
        'user_id':user_id,
        'username':user['dni'],
        'password': req['password']
      }
      self.userPass.createUserPassword(con,creds)
      self.req.removeRequest(con,reqId)

      con.commit()

      response = {'id':pid, 'ok':'usuario creado correctamente'}
      server.sendMessage(response)

      self.sendEvents(server,reqId,user_id)

      self.sendNotificationMail(req)

      return True

    except psycopg2.DatabaseError as e:
        con.rollback()
        raise e

    finally:
        con.close()
