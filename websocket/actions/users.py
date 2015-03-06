# -*- coding: utf-8 -*-
import json, uuid, psycopg2, re
import inject
import hashlib


from model.mail import Mail
from model.users import Users
from model.events import Events
from model.profiles import Profiles
from model.config import Config
from wexceptions import MalformedMessage, AccessDenied

"""
    Modulo de acceso al manejo de usuarios
"""




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


    except psycopg2.DatabaseError, e:

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

  def sendEmail(self, url, hash, email):

      From = self.config.configs['mail_confirm_mail_from']
      To = email
      subject = self.config.configs['mail_confirm_mail_subject']

      ''' falta leer el archivo desde un template y el tema de la url '''

      link = re.sub('\#.*$','#/confirmMail/',url)
      content = '<html><head></head><body><a href="' + link + hash + '">click aqui para confirmar la cuenta</a></body></html>'

      msg = self.mail.createMail(From,To,subject)
      p1 = self.mail.getHtmlPart(content)
      msg.attach(p1)
      self.mail.sendMail(From,[To],msg.as_string())

      return True




  def generateConfirmation(self,con,mail,url):

      hash = hashlib.sha1(mail['id'] + mail['user_id']).hexdigest()
      mail['hash'] = hash
      self.users.updateMail(con,mail)

      ''' envío el mail '''
      self.sendEmail(url,hash,mail['email'])


  def confirm(self,con,mail):
      mail['confirmed'] = True
      self.users.updateMail(con,mail)


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


          self.generateConfirmation(con,mail,message['url'])
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

    except psycopg2.DatabaseError, e:
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
      print json.dumps(response);
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

    except psycopg2.DatabaseError, e:
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
      	  if pattern.search(user["name"]) or pattern.search(user["lastname"]) or pattern.search(user["dni"]):
            rdataAux.append(user)
        rdata = rdataAux

      if 'limit' in message:
        del rdata[message['limit']:]

      if 'onlyIds' in message:
          rdata = map(lambda x: {'id':x['id']}, rdata)

      if 'ids' in message:
          rdata = filter(lambda x: x['id'] in message['ids'], rdata)



      response = {'id':message['id'], 'ok':'', 'users': rdata}
      server.sendMessage(response)
      return True

    finally:
        con.close()
