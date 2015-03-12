# -*- coding: utf-8 -*-
import json, uuid, psycopg2, inject, re, hashlib
from model.requests import Requests
from model.users import Users
from model.students import Students
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
  "action":"rejectAccountRequest",
  "session":"id de session obtenido en el login",
  "description":"motivo del rechazo",
  "reqId":"id del request a eliminar"
}

respuesta:
{
  "id":"id de la peticion"
  O "ok":""
  O "error":""
}

"""


class RejectAccountRequest:

  req = inject.attr(Requests)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)
  mail = inject.attr(Mail)

  def sendEmail(self, request):

      """
        variables a reemplazar :
        ###NAME###
        ###LASTNAME###
        ###DESCRIPTION###
      """

      From = self.config.configs['mail_reject_account_request_from']
      To = request['email']
      subject = self.config.configs['mail_reject_account_request_subject']

      fbody = open('model/systems/accounts/mails/' + self.config.configs['mail_reject_account_request_body'],'r')
      body = fbody.read().decode('utf8')
      fbody.close()

      body = re.sub('###NAME###', unicode(request['name'],'utf-8'), body)
      body = re.sub('###LASTNAME###', unicode(request['lastname'],'utf-8'), body)
      content = re.sub('###DESCRIPTION###', request['description'], body)

      msg = self.mail.createMail(From,To,subject)
      p1 = self.mail.getHtmlPart(content)
      msg.attach(p1)
      self.mail.sendMail(From,[To],msg.as_string())

      return True


  def handleAction(self, server, message):

    if message['action'] != 'rejectAccountRequest':
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

      req = self.req.findRequest(con,rid)
      if (req == None):
          raise MalformedMessage()


      data = req

      if 'description' not in message:
          description = ""
      else:
          description = message['description']

      data['description'] = description;


      self.req.removeRequest(con,rid)
      self.sendEmail(data);
      con.commit()

      response = {'id':pid, 'ok':'petición rechazada correctamente'}
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
    "studentNumber":""
    "name":""
    "lastname":""
    "email":""
    "reason":"",
    "password":""
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
  mail = inject.attr(Mail)
  users = inject.attr(Users)
  students = inject.attr(Students)

  def sendEmail(self, request):

      """
        variables a reemplazar :
        ###NAME###
        ###LASTNAME###
        ###DNI###
        ###URL###
        y dentro de la url config se pueden usar variable :
        ###HASH###
      """

      From = self.config.configs['mail_create_account_request_from']
      To = request['email']
      subject = self.config.configs['mail_create_account_request_subject']
      url = self.config.configs['mail_create_account_request_url']
      url = re.sub('###HASH###', request['hash'], url)

      fbody = open('model/systems/accounts/mails/' + self.config.configs['mail_create_account_request_body'],'r')
      body = fbody.read().decode('utf8')
      fbody.close()

      body = re.sub('###NAME###', request['name'], body)
      body = re.sub('###LASTNAME###', request['lastname'], body)
      body = re.sub('###DNI###', request['dni'], body)
      content = re.sub('###URL###', url, body)

      msg = self.mail.createMail(From,To,subject)
      p1 = self.mail.getHtmlPart(content)
      msg.attach(p1)
      self.mail.sendMail(From,[To],msg.as_string())

      return True



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
    data['hash'] = hashlib.sha1(data['id'] + str(uuid.uuid4())).hexdigest()

    if 'studentNumber' not in data:
        data['studentNumber'] = ''

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      if (self.users.findUserByDni(con,data['dni']) != None):
          response = {'id':message['id'], 'error':'Ya existe el dni registrado a un usuario'}
          server.sendMessage(response)
          return True

      if (data['studentNumber'] != ''):
          if (self.students.findStudentByNumber(con,data['studentNumber']) != None):
              response = {'id':message['id'], 'error':'Ya existe el legajo registrado a un usuario'}
              server.sendMessage(response)
              return True

      self.req.createRequest(con,data)
      self.sendEmail(data)
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
  "id":"id de la peticion"
  "action":"confirmAccountRequest",
  "hash":"hash de la peticion"
}

respuesta:
{
  "id":"id de la peticion"
  O "ok":""
  O "error":""
}

eventos :

AccountRequestConfirmedEvent


"""

class ConfirmAccountRequest:

  req = inject.attr(Requests)
  users = inject.attr(Users)
  profiles = inject.attr(Profiles)
  events = inject.attr(Events)
  mail = inject.attr(Mail)
  userPass = inject.attr(UserPassword)
  config = inject.attr(Config)


  def sendEvents(self,server,req_id):
      event = {
        'type':'AccountRequestConfirmedEvent',
        'data':req_id
      }
      self.events.broadcast(server,event)


  def sendNotificationMail(self,request):
      pass


  def handleAction(self, server, message):

    if message['action'] != 'confirmAccountRequest':
      return False

    pid = message['id']
    hash = message['hash']

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      req = self.req.findRequestByHash(con,hash)
      if (req == None):
          raise MalformedMessage()

      self.req.confirmRequest(con,req['id'])
      con.commit()

      response = {'id':pid, 'ok':'requerimiento confirmado correctamente'}
      server.sendMessage(response)

      self.sendEvents(server,req['id'])

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
  students = inject.attr(Students)



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




  def sendEmail(self, request):

      """
        variables a reemplazar :
        ###NAME###
        ###LASTNAME###
        ###DNI###
      """

      From = self.config.configs['mail_approve_account_request_from']
      To = request['email']
      subject = self.config.configs['mail_approve_account_request_subject']


      fbody = open('model/systems/accounts/mails/' + self.config.configs['mail_approve_account_request_body'],'r')
      body = fbody.read().decode('utf8')
      fbody.close()

      body = re.sub('###NAME###', request['name'], body)
      body = re.sub('###LASTNAME###', request['lastname'], body)
      content = re.sub('###DNI###', request['dni'], body)

      msg = self.mail.createMail(From,To,subject)
      p1 = self.mail.getHtmlPart(content)
      msg.attach(p1)
      self.mail.sendMail(From,[To],msg.as_string())

      return True




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

      mail = {
        'user_id': user_id,
        'email': req['email'],
        'confirmed': req['confirmed']
      }
      self.users.createMail(con,mail)

      ''' uso la clave que pidio en el request '''
      creds = {
        'user_id':user_id,
        'username':user['dni'],
        'password': req['password']
      }
      self.userPass.createUserPassword(con,creds)


      student = {
        'id':user_id,
        'studentNumber':req['studentNumber'],
        'condition':'regular'
      }
      self.students.createStudent(con,student)



      'esto hay que pasarlo a un model - es para habilitar a todo el mundo a au24'
      cur = con.cursor()
      cur.execute('insert into au24.users (id) values (%s)',(user_id,))



      self.req.removeRequest(con,reqId)

      con.commit()

      response = {'id':pid, 'ok':'usuario creado correctamente'}
      server.sendMessage(response)

      self.sendEvents(server,reqId,user_id)

      if mail['confirmed']:
          self.sendEmail(req)

      return True

    except psycopg2.DatabaseError as e:
        con.rollback()
        raise e

    finally:
        con.close()
