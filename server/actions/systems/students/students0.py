
import inject, json
import psycopg2

from model.systems.students.students import Students

from model.events import Events
from model.profiles import Profiles
from model.config import Config

"""
    Modulo de acceso a los datos de los estudiantes
"""


"""
peticion:
{
    "id":"id de la peticion",
    "action":"persistStudent",
    "session":"session de usuario",
    "student": {
        "id":"id del estudiante a actualizar",
        "studentNumber":"legajo",
        "condition":"regularidad del alumno"
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
    'type':'StudentPersistedEvent',
    'data':student['id']
}
"""
class PersistStudent:
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)
  students = inject.attr(Students)

  def handleAction(self, server, message):

    #El procesamiento continuara solo si el mensaje solicitado por el cliente es el que se indica
    if (message['action'] != 'persistStudent'):
      return False

    #Verificar datos del mensaje, si no es correcto responder con un error
    if 'student' not in message:
      response = {'id':message['id'], 'error':'no existe la info del estudiante'}
      server.sendMessage(response)
      return True

    #Verificar rol del usuario conectado a la session
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])

    #Abrir conexion con base de datos
    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      #consultar datos para verificar si existe
      student = message['student']
      studentFromDb = self.students.findStudent(con,student['id'])

      #si no existe estudiante en la base de datos se creara, si existe se actualizara
      if(studentFromDb == None):
        self.students.createStudent(con,student)
      else:
        self.students.updateStudent(con,student)

      con.commit()

      #enviar respuesta al cliente
      response = {'id':message['id'], 'ok':''}
      server.sendMessage(response)

      #enviar evento al cliente
      event = {
        'type':'StudentPersistedEvent',
        'data':student['id']
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
    "action":"createStudent",
    "session":"session de usuario",
    "student": {
        "id":"id del usuario a agregar la info de estudiante",
        "studentNumber":"numero de alumnos",
        "condition":"condicion del alumno"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""
class CreateStudent:

  students = inject.attr(Students)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if (message['action'] != 'createStudent'):
        return False

    if 'student' not in message:
        response = {'id':message['id'], 'error':'no existe la info del estudiante'}
        server.sendMessage(response)
        return True

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:

      student = message['student']
      self.students.createStudent(con,student)
      con.commit()

      response = {'id':message['id'], 'ok':''}
      server.sendMessage(response)

      event = {
        'type':'UserUpdatedEvent',
        'data':student['id']
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
    "action":"findStudent",
    "session":"session de usuario",
    "student": {
        "id":"id del usuario a obtener la info"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "student":{
        "id":"id de la persona",
        "studentNumber":"legajo del alumno",
        "condition":"condicion del alumno"
    }
    "ok":"",
    "error":""
}

"""

class FindStudent:

  students = inject.attr(Students)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if (message['action'] != 'findStudent'):
        return False

    if 'student' not in message:
        response = {'id':message['id'], 'error':'no existe la info del estudiante'}
        server.sendMessage(response)
        return True

    if 'id' not in message['student']:
        response = {'id':message['id'], 'error':'no existe la info del estudiante'}
        server.sendMessage(response)
        return True

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:

      st = message['student']
      student = self.students.findStudent(con,st['id'])
      response = {'id':message['id'], 'student':student, 'ok':''}
      server.sendMessage(response)

      return True

    finally:
        con.close()


"""
peticion:
{
    "id":"",
    "action":"findAllStudents",
    "session":"session de usuario",
}

respuesta:
{
    "id":"id de la peticion",
    "students":[{
        "id":"id de la persona",
        "studentNumber":"legajo del alumno",
        "condition":"condicion del alumno"
    }]
    "ok":"",
    "error":""
}

"""

class FindAllStudents:

  students = inject.attr(Students)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if (message['action'] != 'findAllStudents'):
        return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER','ADMIN-TUTOR','USER-TUTOR'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:

      students = self.students.findAll(con)
      response = {'id':message['id'], 'students':students, 'ok':''}
      server.sendMessage(response)

      return True

    finally:
        con.close()
