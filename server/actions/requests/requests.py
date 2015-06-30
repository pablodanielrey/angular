# -*- coding: utf-8 -*-
import json, uuid, psycopg2, inject, re, hashlib
import logging


from model.objectView import ObjectView

from model.events import Events
from model.requests.requests import Requests
from model.users.users import Users

from model.systems.students.students import Students

from model.profiles import Profiles
from model.mail.mail import Mail
from model.config import Config
from model.credentials.credentials import UserPassword

from model.exceptions import *


"""
    Modulo de acceso a la capa de las peticiones de cuentas.

"""



class AccountRequestMailer:

    config = inject.attr(Config)
    mail = inject.attr(Mail)

    def sendCreateEmail(self, request):

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
      template = self.config.configs['mail_create_account_request_template']

      url = self.config.configs['mail_create_account_request_url']
      url = re.sub('###HASH###', request['hash'], url)

      replace = [
        ('###NAME###',request['name']),
        ('###LASTNAME###',request['lastname']),
        ('###DNI###', request['dni']),
        ('###URL###', url)
      ]

      self.mail.sendMail(From,[To],subject,replace,html=template)

      return True









"""
peticion:
{
  "id":"id de la peticion"
  "action":"resendAccountRequest",
  "session":"id de session obtenido en el login",
  "requests":"requests a reenviar"
}

respuesta:
{
  "id":"id de la peticion"
  O "ok":""
  O "error":""
}

"""


class ResendAccountRequest:

  req = inject.attr(Requests)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)
  mailer = inject.attr(AccountRequestMailer)


  def handleAction(self, server, message):

    if message['action'] != 'resendAccountRequest':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])

    if 'id' not in message:
        raise MalformedMessage()

    if 'requests' not in message:
        raise MalformedMessage()

    pid = message['id']
    requests = message['requests']

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:

        for request in requests:
            rid = request['id'];
            req = self.req.findRequest(con,rid)
            self.mailer.sendCreateEmail(req)

        response = {'id':pid, 'ok':'reenviado correctamente'}
        server.sendMessage(response)

    except Exception as e:
        logging.exception(e)
        response = {'id':pid, 'error':'Error reenviando el eMail'}
        server.sendMessage(response)

    finally:
        con.close()
        return True











"""
peticion:
{
  "id":"id de la peticion"
  "action":"removeAccountRequest",
  "session":"id de session obtenido en el login",
  "requests":"requests a eliminar"
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

    if 'requests' not in message:
        raise MalformedMessage()

    pid = message['id']
    requests = message['requests']

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:

        for request in requests:
            rid = request['id'];
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

      From = self.config.configs['mail_account_request_rejected_from']
      subject = self.config.configs['mail_account_request_rejected_subject']
      template = self.config.configs['mail_account_request_rejected_template']
      To = request['email']

      replace = [
        ('###NAME###',request['name']),
        ('###LASTNAME###',request['lastname']),
        ('###DESCRIPTION###', request['description'])
      ]

      self.mail.sendMail(From,[To],subject,replace,html=template)

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

    except Exception as e:

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
      template = self.config.configs['mail_create_account_request_template']

      url = self.config.configs['mail_create_account_request_url']
      url = re.sub('###HASH###', request['hash'], url)

      replace = [
        ('###NAME###',request['name']),
        ('###LASTNAME###',request['lastname']),
        ('###DNI###', request['dni']),
        ('###URL###', url)
      ]

      self.mail.sendMail(From,[To],subject,replace,html=template)

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
    data['hash'] = hashlib.sha1((data['id'] + str(uuid.uuid4())).encode('utf-8')).hexdigest()

    if 'studentNumber' not in data:
        data['studentNumber'] = ''

    if 'reason' not in data:
        data['reason'] = ''

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
        'type':'AccountRequestCreatedEvent',
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


    def sendEmail(self, request):

        """
            variables a reemplazar :
            ###NAME###
            ###LASTNAME###
            ###DNI###
        """

        From = self.config.configs['mail_account_request_confirmed_from']
        To = request['email']
        subject = self.config.configs['mail_account_request_confirmed_subject']
        template = self.config.configs['mail_account_request_confirmed_template']

        replace = [
            ('###NAME###',request['name']),
            ('###LASTNAME###',request['lastname']),
            ('###DNI###', request['dni'])
        ]

        self.mail.sendMail(From,[To],subject,replace,html=template)

        return True


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

            self.sendEmail(req)

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
  "requests":"peticiones a aprovar"
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

        From = self.config.configs['mail_account_request_aproved_from']
        To = request['email']
        subject = self.config.configs['mail_account_request_aproved_subject']
        template = self.config.configs['mail_account_request_aproved_template']

        replace = [
            ('###NAME###',request['name']),
            ('###LASTNAME###',request['lastname']),
            ('###DNI###', request['dni'])
        ]

        self.mail.sendMail(From,[To],subject,replace,html=template)

        return True



    def handleAction(self, server, message):

        if message['action'] != 'approveAccountRequest':
            return False

        """ chequeo que exista la sesion, etc """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN'])

        pid = message['id']
        requests = message['requests']

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            for request in requests:
                reqId = request['id'];
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

                studentNumber = req['studentNumber']
                studentNumber = studentNumber.strip();
                if (studentNumber != None and studentNumber != ''):
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

                self.sendEvents(server,reqId,user_id)


                if mail['confirmed']:
                    self.sendEmail(req)


            response = {'id':pid, 'ok':'usuario creado correctamente'}
            server.sendMessage(response)

            return True

        except psycopg2.DatabaseError as e:
            con.rollback()
            raise e

        finally:
            con.close()
