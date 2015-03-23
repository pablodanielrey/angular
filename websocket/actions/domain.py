# -*- coding: utf-8 -*-
import inject, json, psycopg2

from model.domain import Domain
from model.events import Events
from model.profiles import Profiles
from model.config import Config
from wexceptions import MalformedMessage

"""
    Modulo de acceso a los datos del dominio
"""


"""
peticion:
{
    "id":"",
    "action":"persistDomainData",
    "session":"sesion de usuario",
    "domain": {
        "id": "id del usuario del dominio"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class PersistDomain:

    req = inject.attr(Domain)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if (message['action'] != 'persistDomainData'):
            return False

        if 'domain' not in message:
            response = {"id":message['id'], 'error':'no existe la info correspondiente al dominio'}
            server.sendMessage(response)
            return True

        if 'id' not in message['domain']:
            response = {"id":message['id'],'error':'el usuario no posee id'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            domain = message['domain']
            self.req.persistDomain(con,domain)
            con.commit()

            response = {'id':message['id'], 'ok':''}
            server.sendMessage(response)

            event = {
                'type':'UserDomainUpdatedEvent',
                'data':domain['id']
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
    "action":"deleteDomainData",
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
    'type':'DomainDeletedEvent',
    'data':domain['id']
}
"""
class DeleteDomain:

    req = inject.attr(Domain)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if message['action'] != 'deleteDomainData':
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
            domain = self.req.findDomain(con,id)
            if domain == None:
                response = {'id':message['id'],'error':'usuario del dominio inexistente'}
                server.send(response)
                return True


            self.req.deleteDomain(con,id)
            con.commit()

            #enviar respuesta al cliente
            response = {'id':message['id'],'ok':''}
            server.sendMessage(response)

            #enviar evento al cliente
            event = {
                'type':'DomainDeletedEvent',
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
    "action":"findDomainData"
    "session":"sesion de usuario"
    "user_id":"id del usuario"
}

respuesta:
{
    "id":"id de la peticion",
    "domain":[
        {
        "id":"id del usuario",
        }
    ],
    "ok":""
    "error":""
}

"""

class FindDomain:

    req = inject.attr(Domain)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if (message['action'] != 'findDomainData'):
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
            domain = self.req.findDomain(con,id)
            response = {'id':message['id'],'ok':'','domain':domain}
            server.sendMessage(response)

            return True

        finally:
            con.close()
