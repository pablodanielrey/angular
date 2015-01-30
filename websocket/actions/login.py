# -*- coding: utf-8 -*-
import psycopg2
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
from wexceptions import MalformedMessage, InsuficientAccess


"""
        Modulo que contiene las clases de acceso a la funcionalidad de login/logout
"""


"""
peticion:
{
    id: "id de la peticion"
    action: "resetPassword"
    username: 'nombre de usuario'
}

respuesta:
{
    id: "id de la peticion",
    ok: 'mensaje de ok, en caso correcto de la generación y envio por correo.'
    error: 'mensaje de error en caso de error'
}
"""


class ResetPassword:

    users = inject.attr(Users)
    userPassword = inject.attr(UserPassword)
    mail = inject.attr(Mail)
    config = inject.attr(Config)


    ''' envío el hash a todos los mails que tenga confirmado el usuario '''
    def sendEmail(self, con, hash, username):

        """
            variables a reemplazar :
            ###DNI###
            ###NAME###
            ###LASTNAME###
            ###URL###
            ###HASH###
        """

        creds = self.userPassword.findCredentials(con,username)
        user_id = creds['user_id']

        user = self.users.findUser(con,user_id)


        From = self.config.configs['mail_reset_password_from']
        subject = self.config.configs['mail_reset_password_subject']
        url = self.config.configs['mail_reset_password_url']
        url = re.sub('###HASH###', hash, url)
        url = re.sub('###USERNAME###', username, url)

        fbody = open('model/systems/accounts/mails/' + self.config.configs['mail_reset_password_body'],'r')
        body = fbody.read().decode('utf8')
        fbody.close()
        body = re.sub('###DNI###', user['dni'], body)
        body = re.sub('###NAME###', user['name'], body)
        body = re.sub('###LASTNAME###', user['lastname'], body)
        content = re.sub('###URL###', url, body)

        mails = self.users.listMails(con,user_id)
        mails = filter(lambda x: x['confirmed'] == True, mails)

        for email in mails:
            To = email['email']

            msg = self.mail.createMail(From,To,subject)
            p1 = self.mail.getHtmlPart(content)
            msg.attach(p1)
            self.mail.sendMail(From,[To],msg.as_string())

        return True



    def handleAction(self, server, message):

        if 'id' not in message:
            raise MalformedMessage()

        if 'action' not in message:
            raise MalformedMessage()

        if message['action'] != 'resetPassword':
            return False

        if 'username' not in message:
            raise MalformedMessage()

        username = message['username']

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            hash = self.userPassword.getResetPasswordHash(con,username)
            self.sendEmail(con, hash, username)

            con.commit()

            response = {'id':message['id'], 'ok':'hash generado correctamente'}
            server.sendMessage(response)

            return True

        finally:
            con.close()


"""
peticion:
{
    id: "id de la peticion"
    action: "changePassword"
    username: 'nombre de usuario'
    password: 'clave a configurar'
    session: "id de session, en caso de cambiar la clave a un usuario logueado"
    hash: "hash generado, en caso de cambiar la clave a un usuario NO logueado (resetPassword)"
}

respuesta:
{
    id: "id de la peticion",
    ok: 'mensaje de ok, en caso correcto del cambio'
    error: 'mensaje de error en caso de error en el cambio'
}
"""

class ChangePassword:

    profiles = inject.attr(Profiles)
    userPassword = inject.attr(UserPassword)
    session = inject.attr(Session)
    config = inject.attr(Config)


    def changePassword(self, con, sid, username, password):
        s = self.session.getSession(sid)
        user_id = s[self.config.configs['session_user_id']]
        creds = self.userPassword.findCredentials(con,username)

        if (creds['user_id'] != user_id):
            ''' se esta tratando de modificar credenciales que pertenecen a otro usuario, no el de la session indicada '''
            if not self.profiles.checkAccess(sid,'ADMIN'):
                raise InsuficientAccess()

        newCreds = {
            'id': creds['id'],
            'user_id': creds['user_id'],
            'username': username,
            'password': password
        }
        self.userPassword.updateUserPassword(con,newCreds);



    def handleAction(self, server, message):

        if 'id' not in message:
            raise MalformedMessage()

        if 'action' not in message:
            raise MalformedMessage()

        if message['action'] != 'changePassword':
            return False

        if 'username' not in message:
            raise MalformedMessage()

        username = message['username']
        password = message['password']


        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            ''' es un reseteo de clave? '''
            if 'hash' in message:

                hash = message['hash']
                self.userPassword.resetUserPassword(con,hash,username,password)

                response = {'id':message['id'], 'ok':'se ha cambiado la clave exitósamente'}
                server.sendMessage(response)

                con.commit()

                return True

            """ es un cambio normal de un usuario logueado """
            """ chequeo que exista la sesion, etc """
            sid = message['session']
            self.profiles.checkAccess(sid,['ADMIN','USER'])

            self.changePassword(con,sid,username,password)

            con.commit()

            response = {'id':message['id'], 'ok':'se ha cambiado la clave exitósamente'}
            server.sendMessage(response)

            return True

        finally:
            con.close()



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
      print str(self.session)

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
    print str(self.session)

    return True
