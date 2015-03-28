# -*- coding: utf-8 -*-
import json, uuid, psycopg2, re
import inject
import hashlib

from model.mail.mail import Mail
from model.users.users import Users
from model.events import Events
from model.profiles import Profiles
from model.config import Config

from wexceptions import *


"""
peticion:
{
    "id":"",
    "action":"removeMail",
    "session":"session de usuario",
    "mail_id":"id del mail a eliminar"
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class RemoveMail:

  users = inject.attr(Users)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if (message['action'] != 'removeMail'):
        return False


    """ chequeo tener permiso como usuario como minimo """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    try:
      con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

      if 'mail_id' not in message:
          response = {'id':message['id'], 'error':''}
          server.sendMessage(response)
          return True

      mail_id = message['mail_id']
      email = self.users.findMail(con,mail_id)
      if email == None:
          response = {'id':message['id'], 'error':'mail inexistente'}
          server.sendMessage(response)
          return True

      ''' chequeo que sea admin para cambiar el mail de otro '''
      local_user_id = self.profiles.getLocalUserId(sid)
      if local_user_id != email['user_id']:
          self.profiles.checkAccess(sid,'ADMIN')

      self.users.deleteMail(con,email['id'])
      con.commit()

      response = {'id':message['id'], 'ok':''}
      server.sendMessage(response)

      event = {
        'type':'UserUpdatedEvent',
        'data':email['user_id']
      }
      self.events.broadcast(server,event)


    except psycopg2.DatabaseError as e:

        response = {'id':message['id'], 'error':''}
        server.sendMessage(response)

    finally:
        if con:
            con.close()

    return True






"""
peticion:
{
    "id":"",
    "action":"confirmMail",
    "sub_action":"generate|confirm",
    "session":"session de usuario",
    "mail_id": "id del email a confirmar"
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class ConfirmMail:

  users = inject.attr(Users)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  mail = inject.attr(Mail)
  config = inject.attr(Config)


  def generateConfirmation(self,con,mail):

      hash = hashlib.sha1((mail['id'] + mail['user_id']).encode('utf-8')).hexdigest()
      mail['hash'] = hash
      self.users.updateMail(con,mail)

      From = self.config.configs['mail_confirm_mail_from']
      subject = self.config.configs['mail_confirm_mail_subject']
      To = mail['email']
      template = self.config.configs['mail_confirm_mail_template']

      url = self.config.configs['mail_confirm_mail_url']
      url = re.sub('###HASH###', hash, url)

      replace = [
          ('###URL###',url)
      ]

      self.mail.sendMail(From,[To],subject,replace,html=template)




  def confirm(self,con,mail):
      mail['confirmed'] = True
      self.users.updateMail(con,mail)

      From = self.config.configs['mail_mail_confirmed_from']
      subject = self.config.configs['mail_mail_confirmed_subject']
      To = mail['email']
      template = self.config.configs['mail_mail_confirmed_template']

      self.mail.sendMail(From,[To],subject,html=template)




  def handleAction(self, server, message):

    if (message['action'] != 'confirmMail'):
        return False

    if 'sub_action' not in message:
        raise MalformedMessage()


    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      if message['sub_action'] == 'generate':

          """ chequeo que sea aunque sea un usuario """
          sid = message['session']
          self.profiles.checkAccess(sid,['ADMIN','USER'])

          email = message['mail_id']
          if email == None:
              response = {'id':message['id'], 'error':''}
              server.sendMessage(response)
              return True

          mail = self.users.findMail(con,email);
          if mail == None:
              response = {'id':message['id'], 'error':'mail inxesistente'}
              server.sendMessage(response)
              return True


          ''' chequeo que sea admin para enviar confirmaciones a mails de otras personas '''
          local_user_id = self.profiles.getLocalUserId(sid)
          if local_user_id != mail['user_id']:
              self.profiles.checkAccess(sid,'ADMIN')


          self.generateConfirmation(con,mail)
          response = {'id':message['id'], 'ok':'email de confirmación enviado'}
          server.sendMessage(response)

          event = {
            'type':'UserUpdatedEvent',
            'data':mail['user_id']
          }
          self.events.broadcast(server,event)

          con.commit()

          return True



      if message['sub_action'] == 'confirm':
          email = message['hash']
          if email == None:
              response = {'id':message['id'], 'error':''}
              server.sendMessage(response)
              return True

          mail = self.users.findMailByHash(con,email);
          if mail == None:
              response = {'id':message['id'], 'error':'mail inxesistente'}
              server.sendMessage(response)
              return True

          self.confirm(con,mail)

          response = {'id':message['id'], 'ok':''}
          server.sendMessage(response)

          event = {
            'type':'UserUpdatedEvent',
            'data':mail['user_id']
          }
          self.events.broadcast(server,event)

          con.commit()

          return True


      raise MalformedMessage()

    except psycopg2.DatabaseError as e:
        con.rollback()
        raise e

    finally:
        con.close()



"""
peticion:
{
    "id":"",
    "action":"listMails"
    "session":"sesion de usuario"
    "user_id":'id de usuario'
}

respuesta:
{
    "id":"id de la petición",
    "mails":[
        {
         "id":"",
         "user_id":"id de usuario",
         "email":"",
         "confirmed":true|false
        }
      ],
    "ok":"",
    "error":""
}

"""

class ListMails:

  users = inject.attr(Users);
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if message['action'] != 'listMails':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      ''' chequeo que sea admin para listar los mails de otras personas '''
      local_user_id = self.profiles.getLocalUserId(sid)
      if local_user_id != message['user_id']:
          self.profiles.checkAccess(sid,'ADMIN')

      rdata = self.users.listMails(con, message['user_id'])
      response = {'id':message['id'], 'ok':'', 'mails': rdata}
      print(json.dumps(response));
      server.sendMessage(response)
      return True

    finally:
        con.close()





"""
peticion:
{
    "id":"",
    "action":"persistMail",
    "session":"session de usuario",
    "mail": {
        "user_id":"id de la persona",
        "email":"email de la persona"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class PersistMail:

  users = inject.attr(Users)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if (message['action'] != 'persistMail'):
        return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      email = message['mail']
      if email == None:
          response = {'id':message['id'], 'error':''}
          server.sendMessage(response)
          return True


      user = self.users.findUser(con,email['user_id']);
      if user == None:
          response = {'id':message['id'], 'error':'usuario inválido'}
          server.sendMessage(response)
          return True


      ''' chequeo que sea admin para crear un mail de otras personas '''
      local_user_id = self.profiles.getLocalUserId(sid)
      if local_user_id != email['user_id']:
          self.profiles.checkAccess(sid,'ADMIN')


      self.users.createMail(con,email);
      con.commit()

      response = {'id':message['id'], 'ok':''}
      server.sendMessage(response)

      event = {
        'type':'UserUpdatedEvent',
        'data':user['id']
      }
      self.events.broadcast(server,event)


    except psycopg2.DatabaseError as e:
        con.rollback()
        raise e

    finally:
        con.close()

    return True
