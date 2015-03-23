# -*- coding: utf-8 -*-
import psycopg2, logging
import inject
import hashlib
import re

from model.profiles import Profiles
from model.mail import Mail
from model.config import Config
from model.events import Events
from model.users import Users
from model.userPassword import UserPassword
from model.session import Session, SessionNotFound

from wexceptions import *


"""
peticion :

{
  "id":"id de la peticion"
  "action":"login",
  "user":"usuario",
  "password":"clave"
}

respuesta :

{
  "id":"id de la peticion"
  "session":"id de sesion a usar para la ejecución de futuras funciones",
  "user_id":'id del usuario logueado'
  "ok":""
  "error":"mensaje de error"
}

"""
class Login:

  userPassword = inject.attr(UserPassword)
  session = inject.attr(Session)
  config = inject.attr(Config)
  events = inject.attr(Events)

  def sendEvents(self,server,user_id):
      event = {
        'type':'StatusChangedEvent',
        'data':''
      }
      self.events.broadcast(server,event)


  def handleAction(self, server, message):

    if message['action'] != 'login':
      return False

    user = message['user']
    passw = message['password']
    credentials = {
        'username':message['user'],
        'password':message['password']
    }

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      rdata = self.userPassword.findUserPassword(con,credentials)
      if rdata == None:
        response = {'id':message['id'], 'error':'autentificación denegada'}
        server.sendMessage(response)
        return True

      sess = {
        self.config.configs['session_user_id']:rdata['user_id'],
        'ip':server.address[0],
        'port':server.address[1]
      }
      sid = self.session.create(sess)

      response = {'id':message['id'], 'ok':'', 'session':sid, 'user_id':rdata['user_id']}
      server.sendMessage(response)

      self.sendEvents(server,rdata['user_id'])

      ''' para debug '''
      print(str(self.session))

      return True

    finally:
        con.close()



"""
peticion :

{
  "id":"id de la peticion"
  "action":"logout",
  "session":"sesion del usuario"
}

respuesta :

{
  "id":"id de la peticion"
 O "ok":""
 O "error":"mensaje de error"
}

"""
class Logout:

  session = inject.attr(Session)
  events = inject.attr(Events)
  config = inject.attr(Config)

  def sendEvents(self,server,user_id):
      event = {
        'type':'StatusChangedEvent',
        'data':''
      }
      self.events.broadcast(server,event)


  def handleAction(self, server, message):

    if message['action'] != 'logout':
      return False

    if 'session' not in message:
        raise MalformedMessage()

    uid = None
    sid = message['session']
    try:
        sess = self.session.findSession(sid)
        uid = sess['data'][self.config.configs['session_user_id']]
        self.session.destroy(sid)
    except SessionNotFound as e:
        pass

    ok = {'id':message['id'], 'ok':''}
    server.sendMessage(ok)

    if uid:
        self.sendEvents(server,uid)

    ''' para debug '''
    print(str(self.session))

    return True
