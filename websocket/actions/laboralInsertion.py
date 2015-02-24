import inject, json
import psycopg2
from model.laboralInsertions import LaboralInsertions
from model.events import Events
from model.profiles import Profiles
from model.config import Config
from wexceptions import MalformedMessage

"""
    Modulo de acceso a los datos de insercion laboral
"""



"""
peticion:
{
    "id":"",
    "action":"createLaboralInsertion",
    "session":"session de usuario",
    "laboralInsertion": {
        "id":"id del usuario a agregar la info de insercion laboral",
        "cv":"curriculum vitae del usario",
        "residir":"si esta dispuesto a residir en otro lugar,
        "viajar":"si esta dispuesto a viajar"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class CreateLaboralInsertion:

    laboralInsertions = inject.attr(LaboralInsertions)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if (message['action'] != 'createLaboralInsertion'):
            return False

        if 'laboralInsertion' not in message:
            response = {'id':message['id'], 'error':'no existe la info correspondiente a insercion laboral '}
            server.sendMessage(response)
            return True

        """ chequeo que exista la sesion, etc """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            laboralInsertion = message['laboralInsertion']
            self.laboralInsertions.createLaboralInsertion(con,laboralInsertion)
            con.commit()

            response = {'id':message['id'], 'ok':''}
            server.sendMessage(response)

            event = {
                'type':'UserUpdatedEvent',
                'data':laboralInsertion['id']
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
    "action":"createLaboralInsertion",
    "session":"session de usuario",
    "laboralInsertion": {
        "id":"id del usuario a agregar la info de insercion laboral",
        "cv":"curriculum vitae del usario",
        "residir":"si esta dispuesto a residir en otro lugar,
        "viajar":"si esta dispuesto a viajar"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class UpdateLaboralInsertion:

    laboralInsertions = inject.attr(LaboralInsertions)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def hanldeAction(self, server, message):

        if (message['action'] != 'updateLaboralInsertion'):
            return False

        if 'laboralInsertion' not in message:
            response = {'id':message['id'], 'error':'no existe la info correspondiente a insercion laboral '}
            server.sendMessage(response)
            return True

        if 'id' not in message['laboralInsertion']:
            response = {'id':message['id'], 'error':'no esta definido el id de insercion laboral '}
            server.sendMessage(response)
            return True

        if message['laboralInsertion']['id'] == None:
            response = {'id':message['id'], 'error':'insercionLaboral.id == null'}
            server.sendMessage(response)
            return True

        """ chequeo que exista la sesion, etc """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            laboralInsertion = message['laboralInsertion']
            if laboralInsertion == None:
                raise MailformedMessage()

            self.laboralInsertions.updateLaboralInsertion(con,laboralInsertion)
            con.commit()

            response = {'id':message['id'], 'ok':''}
            server.sendMessage(response)

            event = {
                'type':'UserUpdatedEvent',
                'data':laboralInsertion['id']
            }
            self.events.boradcast(server,event)
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
    "action":"findLaboralInsertion"
    "session":"sesion de usuario"
    "laboralInsertion":{
        "id":"id de insercion laboral"
    }
}

respuesta:
{
    "id":"id de la petición"
    "laboralInsertion":[
        {
        "id":"id del usuario a agregar la info de insercion laboral",
        "cv":"curriculum vitae del usario",
        "residir":"si esta dispuesto a residir en otro lugar,
        "viajar":"si esta dispuesto a viajar"
        }
    ],
    "ok":""
    "error":""
}

"""

class FindLaboralInsertion:

    laboralInsertions = inject.attr(LaboralInsertions)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if (message['action'] != 'findLaboralInsertion'):
            return False

        """ chequeo que exista la sesion, etc """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            if ((message['laboralInsertion'] == None) or (message['laboralInsertion']['id'] == None)):
                raise MalformedMessage()

            id = message['laboralInsertion']['id']
            laboralInsertion = self.laboralInsertions.findLaboralInsertion(con,id)
            response = {'id':message['id'],'ok':'','laboralInsertion':laboralInsertion}
            server.sendMessage(response)
            return True

        finally:
            con.close()
