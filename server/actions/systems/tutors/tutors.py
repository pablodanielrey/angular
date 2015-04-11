# -*- coding: utf-8 -*-
import inject, psycopg2

from model.systems.tutors.tutors import Tutors
from model.systems.students.students import Students
from model.users.users import Users
from model.events import Events
from model.profiles import Profiles
from model.config import Config

from model.exceptions import *

"""
    Modulo de acceso a los datos de las tutorias
"""



"""
peticion:
{
    "id":"",
    "action":"persistTutorData",
    "session":"session de usuario",
    "request": {
        "date":"fecha ingresada",
        "student": "{ studentNumber:'nro de legajo del alumno',
                      lastname:'apellido del alumno',
                      name:'nombre del alumno',
                      dni:'documento del alumno'
                    }",
        "type":"tipo de relacion"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class PersistTutorData:

    tutors = inject.attr(Tutors)
    events = inject.attr(Events)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    students = inject.attr(Students)
    users = inject.attr(Users)


    def handleAction(self, server, message):

        if (message['action'] != 'persistTutorData'):
            return False

        if 'request' not in message or 'student' not in message['request'] or 'studentNumber' not in message['request']['student']:
            response = {'id':message['id'], 'error':'no existe la info correspondiente a las tutorías'}
            server.sendMessage(response)
            return True

        """ chequeo que exista la sesion, etc """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','ADMIN-TUTOR','USER-TUTOR'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            tutor = message['request']

            # obtengo la persona a ingresar
            student = tutor['student']

            # Verifico si ya existe el alumno ingresado
            s = self.students.findStudentByNumber(con,student['studentNumber'])

            if (s is not None):
                person = self.users.findUser(con,s['id'])
                # si existe, y no tiene los mismos datos tiro error

                if (('dni' in student) and (student['dni'].strip()) and (student['dni'] != person['dni'])):
                    response = {'id':message['id'], 'error':'Error: el alumno ingresado posee otro dni al ingresado (Datos del alumno existente: Dni:' + person['dni'] + ' Apellido:' + person['lastname'] +' Nombre:' + person['name'] +')'}
                    server.sendMessage(response)
                    return True

                # sino, le actualizo los datos con los de la base
                student['lastname'] = person['lastname']
                student['name'] = person['name']
                student['dni'] = person['dni']

            tutor['userId'] = self.profiles.getLocalUserId(sid)


            if 'dni' not  in tutor['student']:
                tutor['student']['dni'] = ''

            if 'name' not in tutor['student']:
                tutor['student']['name'] = ''

            if 'lastname' not in tutor['student']:
                tutor['student']['lastname'] = ''

            self.tutors.persist(con,tutor)
            con.commit()

            response = {'id':message['id'], 'ok':'Registro ingresado correctamente'}
            server.sendMessage(response)

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
    "action":"listTutorData"
    "session":"sesion de usuario"
}

respuesta:
{
    "id":"id de la peticion",
    "response":[
        {
        "user": {
            "dni",
            "name",
            "lastname"
        }
        "date":"fecha",
        "student": {
            "studentNumber",
            "dni",
            "name",
            "lastname"
        }
        "type":"tipo",
        "created":"fecha de creación del registro"
        }
    ],
    "ok":""
    "error":""
}

"""
class ListTutorData:

    tutor = inject.attr(Tutors)
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    users = inject.attr(Users)

    def handleAction(self, server, message):

        if message['action'] != 'listTutorData':
            return False

        #verificar el rol del usuario conectado a la sesion
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','ADMIN-TUTOR'])

        try:
            con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

            tutors = self.tutor.list(con);

            for t in tutors:
                userId = t['userId']
                user = self.users.findUser(con,userId)
                t['user'] = {
                    'dni':user['dni'],
                    'name':user['name'],
                    'lastname':user['lastname']
                }

            response = {'id':message['id'], 'ok':'', 'response':tutors}
            server.sendMessage(response)
            return True

        finally:
            con.close()
