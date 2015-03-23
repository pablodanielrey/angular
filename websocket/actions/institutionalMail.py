# -*- coding: utf-8 -*-
import inject, json, psycopg2

from model.institutionalMail import InstitutionalMail
from model.events import Events
from model.profiles import Profiles
from model.config import Config
from wexceptions import MalformedMessage

"""
    Modulo de acceso a los datos del servidor de correo
"""


"""
peticion:
{
    "id":"",
    "action":"persistUserMailEcono",
    "session":"sesion de usuario",
    "mail": {
        "id": "id del usuario del correo"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class PersistInstitutionalMail:

    req = inject.attr(InstitutionalMail)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if (message['action'] != 'persistUserMailEcono'):
            return False

        if 'mail' not in message:
            response = {"id":message['id'], 'error':'no existe la info correspondiente al usuario de correo'}
            server.sendMessage(response)
            return True

        if 'id' not in message['mail']:
            response = {"id":message['id'],'error':'el usuario no posee id'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            mail = message['mail']
            self.req.persistMail(con,mail)
            con.commit()

            response = {'id':message['id'], 'ok':''}
            server.sendMessage(response)

            event = {
                'type':'UserMailUpdatedEvent',
                'data':mail['id']
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
    "id":"",
    "action":"daleteInstitutionalMail",
    "session":"session de usuario",
    "user_id":"id del usuario a eliminar"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}


evento:
{
    'type':'InstitutionalMailDeletedEvent',
    'data':mail['id']
}
"""
class DeleteInstitutionalMail:

    req = inject.attr(InstitutionalMail)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if message['action'] != 'deleteInstitutionalMail':
            return False

        if 'user_id' not in message:
            response = {'id':message['id'], 'error':'id inexistente'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            id = message['user_id']
            mail = self.req.findMail(con,id)
            if mail == None:
                response = {'id':message['id'],'error':'usuario del servidor del correo inexistente'}
                server.send(response)
                return True


            self.req.deleteMail(con,id)
            con.commit()

            #enviar respuesta al cliente
            response = {'id':message['id'],'ok':''}
            server.sendMessage(response)

            #enviar evento al cliente
            event = {
                'type':'InstitutionalMainDeletedEvent',
                'data':id
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
    "id":"",
    "action":"findInstitutionalMailData"
    "session":"sesion de usuario"
    "user_id":"id del usuario"
}

respuesta:
{
    "id":"id de la peticion",
    "mail":[
        {
        "id":"id del usuario",
        }
    ],
    "ok":""
    "error":""
}

"""

class FindInstitutionalMail:

    req = inject.attr(InstitutionalMail)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if (message['action'] != 'findInstitutionalMailData'):
            return False

        if 'user_id' not in message:
            response = {'id':message['id'], 'error':'id inexistente'}
            server.sendMessage(response)
            return True

        """ chequeo que exista la sesion, etc """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            id = message['user_id']
            mail = self.req.findMail(con,id)
            response = {'id':message['id'],'ok':'','mail':mail}
            server.sendMessage(response)
            return True

        finally:
            con.close()
