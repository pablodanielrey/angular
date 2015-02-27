import inject, json
import psycopg2
from model.laboralInsertion import LaboralInsertion
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
    "action":"persistLaboralInsertionData",
    "session":"session de usuario",
    "laboralInsertion": {
        "id":"id del usuario a agregar la info de insercion laboral",
        "cv":"curriculum vitae del usario",
        "reside":"si esta dispuesto a residir en otro lugar,
        "travel":"si esta dispuesto a viajar"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class PersistLaboralInsertion:

    laboralInsertion = inject.attr(LaboralInsertion)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if (message['action'] != 'persistLaboralInsertionData'):
            return False

        if 'laboralInsertion' not in message:
            response = {'id':message['id'], 'error':'no existe la info correspondiente a insercion laboral '}
            server.sendMessage(response)
            return True

        """ chequeo que exista la sesion, etc """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            laboralInsertion = message['laboralInsertion']
            self.laboralInsertion.persistLaboralInsertion(con,laboralInsertion)
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
    "action":"findLaboralInsertion"
    "session":"sesion de usuario"
    "laboralInsertion":{
        "id":"id de insercion laboral"
    }
}

respuesta:
{
    "id":"id de la peticion",
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

    LaboralInsertion = inject.attr(LaboralInsertion)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if (message['action'] != 'findLaboralInsertionData'):
            return False


        """ chequeo que exista la sesion, etc """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            if ((message['laboralInsertion'] == None) or (message['laboralInsertion']['id'] == None)):
                raise MalformedMessage()

            id = message['laboralInsertion']['id']
            laboralInsertion = self.LaboralInsertion.findLaboralInsertion(con,id)
            response = {'id':message['id'],'ok':'','laboralInsertion':laboralInsertion}
            server.sendMessage(response)
            return True

        finally:
            con.close()


"""-------------------------------"""
"""
    Modulo de acceso a los datos de los idiomas del usuario
"""

"""
peticion:
{
    "id":"id de la peticion",
    "action":"createLanguagesData",
    "session":"session de usuario",
    "user_id":"id del usuario"
    "language": [
            {
            "id":"id del idioma a actualizar",
            "user_id":"id del usuario",
            "name":"nombre del idioma",
            "level":"nivel"
            }
    ]
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class CreateLanguages:

    req = inject.attr(LaboralInsertion)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if message['action'] != 'createLanguagesData':
            return False

        if 'user_id' not in message:
            response = {'id':message['id'],'error':'no existe el id del usuario'}

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            #elimino todos los idomas del usuario
            self.req.deleteDegrees(con,message['user_id'])

            #verifico que se hayan mandado idiomas en el mensaje
            if 'language' in message:
                #agrego todos los idiomas
                languages = message['language']
                for l in languages:
                    self.req.persistLanguage(con,l)

            con.commit()

            response = {'id':message['id'],'ok':''}
            server.sendMessage(response)
            self.events.broadcast(server,event)

        except psycopg2.DatabaseError, e:
            con.rollback()
            raise e

        finally:
            con.close()




"""
peticion:
{
    "id":"id de la peticion",
    "action":"persistLanguage",
    "session":"session de usuario",
    "language": {
        "id":"id del lenguaje a actualizar",
        "user_id":"id del usuario",
        "name":"nombre del lenguaje",
        "level":"nivel"
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
    'type':'LanguagePersistedEvent',
    'data':language['id']
}
"""

class PersistLanguage:

    req = inject.attr(LaboralInsertion)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):
        #El procesamiento continuara solo si el mensaje solicitado por el cliente es el que se indica
        if (message['action'] != 'persistLanguage'):
            return False

        #Verificar datos del mensaje, si no es correcto responder con un error
        if 'language' not in message:
            response = {'id':messages['id'], 'error':'no existe la info del lenguaje'}
            server.sendMessage(response)
            return True

        #Verificar rol del usuario conectado a la session
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            #Abrir conexion con base de datos
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            #persistir el dato en la base
            language = message['language']
            self.req.persistLanguage(con,language)
            con.commit()

            #enviar respuesta al cliente
            response = {'id':message['id'],'ok':''}
            server.sendMessage(response)

            #enviar evento al cliente
            event = {
                'type':'LanguagePersistedEvent',
                'data':language['id']
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
    "action":"removeLanguage",
    "session":"session de usuario",
    "language": {
        id:"id del lenguaje a eliminar"
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
    'type':'LanguageDeletedEvent',
    'data':language['id']
}
"""
class DeleteLanguage:

    req = inject.attr(LaboralInsertion)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):
        #El procesamiento continuara solo si el mensaje solicitado por el cliente es el que se indica
        if message['action'] != 'removeLanguage':
            return False

        #Verificar datos del mensaje, si no es correcto responder con un error
        if 'language' not in message:
            response = {'id':message['id'], 'error':'no existe la info del lenguaje'}
            server.sendMessage(response)
            return True

        if 'id' not in message['language']:
            response = {'id':message['id'], 'error': 'language.id == null'}
            server.sendMessage(response)
            return True

        #Verificar rol del usuario conectado a la session
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            #Abrir conexion con base de datos
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            #buscar si existe el lenguaje
            l = message['language']
            language = self.req.findLanguage(con,l['id'])
            if language == None:
                response = {'id':message['id'],'error':'lenguaje inexistente'}
                server.send(response)
                return True

            #eliminar el lenguaje
            self.req.deleteLanguage(con,l['id'])

            #enviar respuesta al cliente
            response = {'id':message['id'],'ok':''}
            server.sendMessage(response)

            #enviar evento al cliente
            event = {
                'type':'LanguageDeletedEvent',
                'data':language['id']
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
    "action":"findLanguage"
    "session":"sesion de usuario"
    "language":{
        "id":"id del idioma"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "language":[
        {
        "id":"id del idioma a actualizar",
        "user_id":"id del usuario",
        "name":"nombre del idioma",
        "level":"nivel"
        }
    ],
    "ok":""
    "error":""
}

"""
class FindLanguage:

    req = inject.attr(LaboralInsertion)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        #El procesamiento continuara solo si el mensaje solicitado por el cliente es el que se indica
        if message['action'] != 'findLanguageData':
            return False

        #Verificar datos del mensaje, si no es correcto responder con un error
        if 'language' not in message:
            response = {'id':message['id'], 'error':'no existe la info del idioma'}
            server.sendMessage(response)
            return True

        if 'id' not in message['language']:
            response = {'id':message['id'], 'error':'language.id == null'}
            server.sendMessage(response)
            return True

        #verificar rol del usuario conectado a la sesion
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            #Abrir conexion a la base de datos
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            #realizo la consulta al modelo
            l = message['language']
            language = self.req.findLanguage(con,l['id'])
            response = {'id':message['id'], 'language':language, 'ok':''}
            server.sendMessage(response)

            return True

        finally:
            con.close()

"""

peticion:
{
    "id":"",
    "action":"listLanguageData"
    "session":"sesion de usuario"
    "user_id":"id del usuario del cual se necesitan sus idiomas"
}

respuesta:
{
    "id":"id de la peticion",
    "languages":[
        {
        "id":"id del idioma a actualizar",
        "user_id":"id del usuario",
        "name":"nombre del idioma",
        "level":"nivel"
        }
    ],
    "ok":""
    "error":""
}

"""
class ListLanguages:

    req = inject.attr(LaboralInsertion)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        #El procesamiento continuara solo si el mensaje solicitando por el cliente es el que se indica
        if message['action'] != 'listLanguageData':
            return False

        #verificar datos del mensaje, si no es correcto responder con un error
        if 'user_id' not in message:
            response = {'id':message['id'], 'error':'no existe el id del usuario'}
            server.sendMessage(response)
            return True

        #verificar el rol del usuario conectado a la sesion
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            #Abrir conexion a la base de datos
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            #realizo la consulta al modelo
            languages = self.req.listLanguages(con, message['user_id'])
            response = {'id':message['id'], 'ok':'', 'languages':languages}
            server.sendMessage(response)
            return True

        finally:
            con.close()


"""-------------------------------"""
"""
    Modulo de acceso a los datos de las carreras del usuario
"""



"""
peticion:
{
    "id":"id de la peticion",
    "action":"createDegreesData",
    "session":"session de usuario",
    "user_id":"id del usuario"
    "degree": [
            {
            'id':'id de la carrera',
            'user_id':'id del usuario',
            'name':'nombre de la carrera',
            'curses':'materias aprobadas',
            'average1':'promedio con aplazo',
            'average2':'promedio sin aplazo',
            'work_type': 'lista de tipos de trabajos solicitados'
            }
    ]
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class CreateDegrees:

    req = inject.attr(LaboralInsertion)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if message['action'] != 'createDegreesData':
            return False

        if 'user_id' not in message:
            response = {'id':message['id'],'error':'no existe el id del usuario'}

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            #elimino todas las carreras que posea el usuario
            self.req.deleteDegrees(con,message['user_id'])

            #verifico que se hayan mandado carreras en el mensaje
            if 'degree' in message:
                #agrego todas las carreras
                degrees = message['degree']
                for d in degrees:
                    self.req.persistDegree(con,d)

            con.commit()

            response = {'id':message['id'],'ok':''}
            server.sendMessage(response)
            self.events.broadcast(server,event)

        except psycopg2.DatabaseError, e:
            con.rollback()
            raise e

        finally:
            con.close()

"""
peticion:
{
    "id":"id de la peticion",
    "action":"persistDegreeData",
    "session":"session de usuario",
    "degree": {
            'id':'id de la carrera',
            'user_id':'id del usuario',
            'name':'nombre de la carrera',
            'curses':'materias aprobadas',
            'average1':'promedio con aplazo',
            'average2':'promedio sin aplazo',
            'work_type': 'lista de tipos de trabajos solicitados'
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
    'type':'DegreePersistedEvent',
    'data':degree['id']
}
"""

class PersistDegree:

    req = inject.attr(LaboralInsertion)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):
        if message['action'] != 'persistDegreeData':
            return False

        if 'degree' not in message:
            response = {'id':message['id'], 'error:': 'no existe la info de la carrera'}
            server.sendMessage(response)
            return True


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'],dbname=self.config.configs['database_database'],user=self.config.configs['database_user'],password=self.config.configs['database_password'])

            degree = message['degree']
            self.req.persistDegree(con,degree)
            con.commit()

            response = {'id':message['id'],'ok':''}
            server.sendMessage(response)

            event = {
                'type':'DegreePersistedEvent',
                'data':degree['id']
            }
            self.events.broadcast(server,event)

            return True

        except psycopg2.DatabaseError, e:
            con.roolback()
            raise e

        finally:
            con.close()

"""
peticion:
{
    "id":"id de la peticion",
    "action":"removeDegreeData",
    "session":"session de usuario",
    "degree": {
            'id':'id de la carrera',
            'user_id':'id del usuario',
            'name':'nombre de la carrera',
            'curses':'materias aprobadas',
            'average1':'promedio con aplazo',
            'average2':'promedio sin aplazo',
            'work_type': 'lista de tipos de trabajos solicitados'
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
    'type':'DegreeDeletedEvent',
    'data':degree['id']
}
"""
class DeleteDegree:

    req = inject.attr(LaboralInsertion)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if message['action'] != 'removeDegreeData':
            return False

        if 'degree' not in message:
            reponse = {'id':message['id'],'error':'no existe la info de la carrera'}
            server.sendMessage(response)
            return True

        if 'id' not in message['degree']:
            respnse = {'id':message['id'],'error':'carrera.id = null'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            d = message['degree']
            degree = self.req.findDegree(con,d['id'])
            if degree == None:
                response = {'id':message['id'],'error':'carrera inexistente'}
                server.sendMessage(response)
                return True

            self.req.deleteDegree(con,d['id'])

            event = {
                'type':'DegreeDeletedEvent',
                'data':degree['id']
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
    "action":"findDegree"
    "session":"sesion de usuario"
    "degree":{
        "id":"id de la carrera"
    }
}

respuesta:
{
    "id":"id de la peticion",

    "degree": {
            'id':'id de la carrera',
            'user_id':'id del usuario',
            'name':'nombre de la carrera',
            'curses':'materias aprobadas',
            'average1':'promedio con aplazo',
            'average2':'promedio sin aplazo',
            'work_type': 'lista de tipos de trabajos solicitados'
    }
    "ok":""
    "error":""
}

"""
class FindDegree:

    req = inject.attr(LaboralInsertion)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if message['action'] != 'findDegree':
            return False

        if 'degree' not in message:
            response = {'id':message['id'],'error':'no existe la info de la carrera'}
            server.sendMessage(response)
            return True

        if 'id' not in message['degree']:
            response = {'id':message['id'],'error':'carrera.id = null'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            d = message['degree']
            degree = self.req.findDegree(con,d['id'])
            response = {'id':message['id'], 'degree':degree,'ok':''}
            server.sendMessage(response)

            return True

        finally:
            con.close()
"""

peticion:
{
    "id":"",
    "action":"listDegrees"
    "session":"sesion de usuario"
    'user_id':"id de usuario"
}

respuesta:
{
    "id":"id de la peticion",

    "degree": [
            {
            'id':'id de la carrera',
            'user_id':'id del usuario',
            'name':'nombre de la carrera',
            'curses':'materias aprobadas',
            'average1':'promedio con aplazo',
            'average2':'promedio sin aplazo',
            'work_type': 'lista de tipos de trabajos solicitados'
            }
    ]
    "ok":""
    "error":""
}

"""
class ListDegree:

    req = inject.attr(LaboralInsertion)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if message['action'] != 'listDegrees':
            return False

        if 'user_id' not in message:
            response = {'id':message['id'],'error':'no existe el id del usuario'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            degrees = self.req.listDegrees(con,message['user_id'])
            response = {'id':message['id'],'ok':'','degrees':degrees}
            server.sendMessage(response)

            return True

        finally:
            con.close()


"""-------------------------------"""

"""

peticion:
{
    "id":"",
    "action":"acceptTermsAndConditions"
    "session":"sesion de usuario"
    "user_id":"id del usuario"
}

respuesta:
{
    "id":"id de la peticion",
    "ok":""
    "error":""
}

"""
class AcceptTermsAndConditions:

    req = inject.attr(LaboralInsertion)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        #El procesamiento continuara solo si el mensaje solicitado por el cliente es el que indica
        if message['action'] != 'acceptTermsAndConditions':
            return False


        if 'user_id' not in message:
            response = {'id':message['id'],'error':'no existe el usuario'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            #Abrir conexion a la base de datos
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            self.req.acceptTermsAndConditions(con,message['user_id'])
            response = {'id':message['id'],'ok':''}
            server.sendMessage(response)

            con.commit()

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
    "action":"checkTermsAndConditions"
    "session":"sesion de usuario"
    "user_id":"id del usuario"
}

respuesta:
{
    "id":"id de la peticion",
    "accepted":"verifica si ya acepto los terminos y condiciones"
    "ok":""
    "error":""
}

"""
class CheckTermsAndConditions:

    req = inject.attr(LaboralInsertion)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        #El procesamiento continuara solo si el mensaje solicitado por el cliente es el que indica
        if message['action'] != 'checkTermsAndConditions':
            return False

        if 'user_id' not in message:
            response = {'id':message['id'], 'error':'no existe el id del usuario'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])

        try:
            #Abrir conexion a la base de datos
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            #realizo la consulta al modelo
            accepted = self.req.checkTermsAndConditions(con,message['user_id'])
            response = {'id':message['id'],'accepted':accepted, 'ok':''}
            server.sendMessage(response)
            return True

        finally:
            con.close()
